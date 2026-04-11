from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.schemas import HeartRiskRequest, HeartRiskResponse


PRODUCTION_MODEL_PATH = Path("models/best_production.joblib")
BASELINE_MODEL_PATH = Path("models/best_baseline.joblib")
REPORT_DIR = Path("reports")
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

    if PRODUCTION_MODEL_PATH.exists():
        _model_bundle = joblib.load(PRODUCTION_MODEL_PATH)
        _model_source = str(PRODUCTION_MODEL_PATH)
        return

    if BASELINE_MODEL_PATH.exists():
        _model_bundle = joblib.load(BASELINE_MODEL_PATH)
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

    row = pd.DataFrame([payload.model_dump()])[FEATURE_ORDER]
    probability = float(_model_bundle["model"].predict_proba(row)[0, 1])
    threshold = float(_model_bundle.get("threshold", 0.5))
    label = "high_risk" if probability >= threshold else "low_risk"

    estimator_name = _model_bundle["model"].named_steps["classifier"].__class__.__name__

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

    if metrics_summary_path.exists():
        metrics_summary = json.loads(metrics_summary_path.read_text(encoding="utf-8"))

    if explainability_summary_path.exists():
        explainability_summary = json.loads(explainability_summary_path.read_text(encoding="utf-8"))

    if model_comparison_path.exists():
        model_comparison_markdown = model_comparison_path.read_text(encoding="utf-8")

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
        "top_features": top_features,
        "available_images": available_images,
    }
