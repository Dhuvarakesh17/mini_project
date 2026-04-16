from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import torch
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from torch import nn

from src.api.schemas import HeartRiskRequest, HeartRiskResponse


DEEP_MODEL_STATE_PATH = Path("models/heart_net_state.pt")
DEEP_PREPROCESSOR_PATH = Path("models/heart_net_preprocessor.joblib")
DEEP_METRICS_PATH = Path("models/deep_metrics.json")
PRODUCTION_MODEL_PATH = Path("models/best_production.joblib")
BASELINE_MODEL_PATH = Path("models/best_baseline.joblib")
BASELINE_METRICS_PATH = Path("models/baseline_metrics.json")
REPORT_DIR = Path("reports")
LATEST_PREDICTION_REPORT_PATH = REPORT_DIR / "latest_prediction_report.json"
FEATURE_ORDER = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
]


class HeartNet(nn.Module):
    def __init__(self, input_dim: int) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


def _load_deep_bundle() -> dict[str, Any] | None:
    if not (
        DEEP_MODEL_STATE_PATH.exists()
        and DEEP_PREPROCESSOR_PATH.exists()
        and DEEP_METRICS_PATH.exists()
    ):
        return None

    deep_meta = json.loads(DEEP_METRICS_PATH.read_text(encoding="utf-8"))
    input_dim = int(deep_meta.get("input_dim", 28))
    threshold = float(deep_meta.get("threshold", 0.5))
    feature_order = deep_meta.get("feature_order") or FEATURE_ORDER

    model = HeartNet(input_dim=input_dim)
    state_dict = torch.load(DEEP_MODEL_STATE_PATH, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()

    preprocessor = joblib.load(DEEP_PREPROCESSOR_PATH)

    return {
        "mode": "deep",
        "model": model,
        "preprocessor": preprocessor,
        "threshold": threshold,
        "feature_order": feature_order,
        "model_name": "HeartNet (Deep Learning)",
    }


def _build_prediction_insights(payload: HeartRiskRequest) -> list[str]:
    insights: list[str] = []

    if payload.age >= 55:
        insights.append("Age is in a higher-risk range for heart problems.")
    if payload.trestbps >= 140:
        insights.append("Resting blood pressure is elevated.")
    if payload.chol >= 240:
        insights.append("Cholesterol is above the desirable level.")
    if payload.fbs == 1:
        insights.append("Fasting blood sugar suggests possible glucose-related risk.")
    if payload.exang == 1:
        insights.append("Chest pain during exercise is a strong warning signal.")
    if payload.oldpeak >= 2:
        insights.append("Exercise ECG stress change is noticeably elevated.")
    if payload.ca >= 2:
        insights.append("Multiple major vessels are flagged in imaging-based input.")
    if payload.thalach < 120:
        insights.append("Lower peak heart rate may indicate reduced exercise tolerance.")

    if not insights:
        insights.append("No strong high-risk signals were detected in key inputs.")

    return insights[:6]


def _build_follow_up_recommendation(risk_label: str, risk_probability: float) -> str:
    if risk_label == "high_risk" and risk_probability >= 0.8:
        return "Please seek urgent evaluation from a heart specialist."
    if risk_label == "high_risk":
        return "Please book a medical follow-up soon for full clinical assessment."
    if risk_probability >= 0.35:
        return "Risk is lower than threshold, but regular monitoring and lifestyle care are advised."
    return "Maintain healthy routines and continue routine health checkups."


def _save_latest_prediction_report(
    payload: HeartRiskRequest,
    risk_probability: float,
    threshold: float,
    risk_label: str,
    model_name: str,
) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model_name": model_name,
        "risk_probability": risk_probability,
        "threshold": threshold,
        "risk_label": risk_label,
        "summary": (
            "Higher chance of heart problem"
            if risk_label == "high_risk"
            else "Lower chance of heart problem"
        ),
        "recommendation": _build_follow_up_recommendation(risk_label, risk_probability),
        "insights": _build_prediction_insights(payload),
        "inputs": payload.model_dump(),
    }
    LATEST_PREDICTION_REPORT_PATH.write_text(
        json.dumps(report_payload, indent=2),
        encoding="utf-8",
    )


def _build_model_comparison_table() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    if BASELINE_METRICS_PATH.exists():
        baseline = json.loads(BASELINE_METRICS_PATH.read_text(encoding="utf-8"))
        selected_name = baseline.get("selected_model")
        selected_metrics = baseline.get("model_results", {}).get(selected_name, {})
        rows.append(
            {
                "model": f"Baseline ({selected_name})",
                "roc_auc": float(selected_metrics.get("roc_auc", 0.0)),
                "pr_auc": float(selected_metrics.get("pr_auc", 0.0)),
                "recall": float(selected_metrics.get("recall", 0.0)),
                "specificity": float(selected_metrics.get("specificity", 0.0)),
                "f1": float(selected_metrics.get("f1", 0.0)),
            }
        )

    if DEEP_METRICS_PATH.exists():
        deep = json.loads(DEEP_METRICS_PATH.read_text(encoding="utf-8"))
        metrics = deep.get("metrics", {})
        rows.append(
            {
                "model": "HeartNet (Deep Learning)",
                "roc_auc": float(metrics.get("roc_auc", 0.0)),
                "pr_auc": float(metrics.get("pr_auc", 0.0)),
                "recall": float(metrics.get("recall", 0.0)),
                "specificity": float(metrics.get("specificity", 0.0)),
                "f1": float(metrics.get("f1", 0.0)),
            }
        )

    return rows

app = FastAPI(title="Heart Disease Risk API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/reports-assets", StaticFiles(directory=REPORT_DIR, check_dir=False), name="reports-assets")

_model_bundle = None
_model_source = None


@app.on_event("startup")
def load_model() -> None:
    global _model_bundle
    global _model_source

    deep_bundle = _load_deep_bundle()
    if deep_bundle is not None:
        _model_bundle = deep_bundle
        _model_source = str(DEEP_MODEL_STATE_PATH)
        return

    if PRODUCTION_MODEL_PATH.exists():
        loaded_bundle = joblib.load(PRODUCTION_MODEL_PATH)
        loaded_bundle["mode"] = "classification"
        _model_bundle = loaded_bundle
        _model_source = str(PRODUCTION_MODEL_PATH)
        return

    if BASELINE_MODEL_PATH.exists():
        loaded_bundle = joblib.load(BASELINE_MODEL_PATH)
        loaded_bundle["mode"] = "classification"
        _model_bundle = loaded_bundle
        _model_source = str(BASELINE_MODEL_PATH)
        return

    if not PRODUCTION_MODEL_PATH.exists() and not BASELINE_MODEL_PATH.exists():
        _model_bundle = None
        _model_source = None
        return


@app.get("/health")
def health() -> dict:
    model_ready = _model_bundle is not None
    return {"status": "ok", "model_ready": model_ready, "model_source": _model_source}


@app.post("/predict", response_model=HeartRiskResponse)
def predict(payload: HeartRiskRequest) -> HeartRiskResponse:
    if _model_bundle is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Train baseline or advanced model first.")

    row = pd.DataFrame([payload.model_dump()])

    if _model_bundle.get("mode") == "deep":
        feature_order = _model_bundle.get("feature_order", FEATURE_ORDER)
        transformed = _model_bundle["preprocessor"].transform(row[feature_order])
        transformed_array = transformed.toarray() if hasattr(transformed, "toarray") else np.asarray(transformed)
        x_tensor = torch.tensor(np.asarray(transformed_array), dtype=torch.float32)

        with torch.no_grad():
            logits = _model_bundle["model"](x_tensor).squeeze(dim=1)
            probability = float(torch.sigmoid(logits).cpu().numpy()[0])

        estimator_name = _model_bundle.get("model_name", "HeartNet (Deep Learning)")
    else:
        ordered_row = row[FEATURE_ORDER]
        probability = float(_model_bundle["model"].predict_proba(ordered_row)[0, 1])
        estimator_name = _model_bundle["model"].named_steps["classifier"].__class__.__name__

    threshold = float(_model_bundle.get("threshold", 0.5))
    label = "high_risk" if probability >= threshold else "low_risk"

    _save_latest_prediction_report(payload, probability, threshold, label, estimator_name)

    return HeartRiskResponse(
        risk_probability=probability,
        threshold=threshold,
        risk_label=label,
        model_name=estimator_name,
    )


@app.get("/reports/summary")
def reports_summary() -> dict:
    if not REPORT_DIR.exists():
        raise HTTPException(status_code=404, detail="Reports directory not found. Generate reports first.")

    metrics_summary_path = REPORT_DIR / "metrics_summary.json"
    explainability_summary_path = REPORT_DIR / "explainability_summary.json"
    model_comparison_path = REPORT_DIR / "model_comparison.md"
    feature_importance_path = REPORT_DIR / "feature_importance_permutation.json"

    metrics_summary = {}
    explainability_summary = {}
    model_comparison_markdown = ""
    top_features: list[dict] = []
    latest_prediction_report: dict[str, Any] = {}

    if metrics_summary_path.exists():
        metrics_summary = json.loads(metrics_summary_path.read_text(encoding="utf-8"))

    if explainability_summary_path.exists():
        explainability_summary = json.loads(explainability_summary_path.read_text(encoding="utf-8"))

    if model_comparison_path.exists():
        model_comparison_markdown = model_comparison_path.read_text(encoding="utf-8")

    if LATEST_PREDICTION_REPORT_PATH.exists():
        latest_prediction_report = json.loads(LATEST_PREDICTION_REPORT_PATH.read_text(encoding="utf-8"))

    if feature_importance_path.exists():
        feature_data = json.loads(feature_importance_path.read_text(encoding="utf-8"))
        top_features = sorted(feature_data, key=lambda item: item.get("importance_mean", 0), reverse=True)[:8]

    image_files = [
        "baseline_roc_curve.png",
        "baseline_pr_curve.png",
        "baseline_confusion_matrix.png",
        "baseline_calibration_curve.png",
        "feature_importance_permutation.png",
    ]
    available_images = [name for name in image_files if (REPORT_DIR / name).exists()]

    return {
        "metrics_summary": metrics_summary,
        "explainability_summary": explainability_summary,
        "model_comparison_markdown": model_comparison_markdown,
        "model_comparison_table": _build_model_comparison_table(),
        "top_features": top_features,
        "available_images": available_images,
        "latest_prediction_report": latest_prediction_report,
    }
