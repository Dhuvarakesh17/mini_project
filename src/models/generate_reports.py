from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    auc,
    precision_recall_curve,
    roc_curve,
)
from sklearn.model_selection import train_test_split

from src.data.load_dataset import get_feature_target, load_cleveland_dataset


RAW_DATA_PATH = Path("data/raw/processed_cleveland.csv")
MODEL_DIR = Path("models")
REPORT_DIR = Path("reports")
SEED = 42


def _save_roc_curve(y_true: np.ndarray, y_prob: np.ndarray, output_path: Path) -> None:
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, label=f"ROC AUC = {roc_auc:.3f}", linewidth=2)
    plt.plot([0, 1], [0, 1], linestyle="--", linewidth=1)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Baseline ROC Curve")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=140)
    plt.close()


def _save_pr_curve(y_true: np.ndarray, y_prob: np.ndarray, output_path: Path) -> None:
    precision, recall, _ = precision_recall_curve(y_true, y_prob)

    plt.figure(figsize=(7, 5))
    plt.plot(recall, precision, linewidth=2)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Baseline Precision-Recall Curve")
    plt.tight_layout()
    plt.savefig(output_path, dpi=140)
    plt.close()


def _save_confusion_matrix(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float,
    output_path: Path,
) -> None:
    y_pred = (y_prob >= threshold).astype(int)

    plt.figure(figsize=(6, 5))
    disp = ConfusionMatrixDisplay.from_predictions(
        y_true,
        y_pred,
        display_labels=["no_disease", "disease"],
        cmap="YlOrRd",
        colorbar=False,
    )
    disp.ax_.set_title(f"Confusion Matrix (threshold={threshold:.2f})")
    plt.tight_layout()
    plt.savefig(output_path, dpi=140)
    plt.close()


def _save_calibration_curve(y_true: np.ndarray, y_prob: np.ndarray, output_path: Path) -> None:
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10, strategy="uniform")

    plt.figure(figsize=(7, 5))
    plt.plot(prob_pred, prob_true, marker="o", linewidth=2)
    plt.plot([0, 1], [0, 1], linestyle="--", linewidth=1)
    plt.xlabel("Mean Predicted Probability")
    plt.ylabel("Fraction of Positives")
    plt.title("Baseline Calibration Curve")
    plt.tight_layout()
    plt.savefig(output_path, dpi=140)
    plt.close()


def _write_model_comparison(baseline_metrics_path: Path, deep_metrics_path: Path, output_path: Path) -> None:
    lines = [
        "# Model Comparison",
        "",
        "| Model | ROC-AUC | PR-AUC | Recall (Sensitivity) | Specificity | F1 |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    if baseline_metrics_path.exists():
        baseline = json.loads(baseline_metrics_path.read_text(encoding="utf-8"))
        selected_name = baseline.get("selected_model")
        selected_metrics = baseline.get("model_results", {}).get(selected_name, {})
        lines.append(
            "| baseline_selected ({}) | {:.3f} | {:.3f} | {:.3f} | {:.3f} | {:.3f} |".format(
                selected_name,
                float(selected_metrics.get("roc_auc", 0.0)),
                float(selected_metrics.get("pr_auc", 0.0)),
                float(selected_metrics.get("recall", 0.0)),
                float(selected_metrics.get("specificity", 0.0)),
                float(selected_metrics.get("f1", 0.0)),
            )
        )

    if deep_metrics_path.exists():
        deep = json.loads(deep_metrics_path.read_text(encoding="utf-8"))
        metrics = deep.get("metrics", {})
        lines.append(
            "| deep_heart_net | {:.3f} | {:.3f} | {:.3f} | {:.3f} | {:.3f} |".format(
                float(metrics.get("roc_auc", 0.0)),
                float(metrics.get("pr_auc", 0.0)),
                float(metrics.get("recall", 0.0)),
                float(metrics.get("specificity", 0.0)),
                float(metrics.get("f1", 0.0)),
            )
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    production_path = MODEL_DIR / "best_production.joblib"
    baseline_path = MODEL_DIR / "best_baseline.joblib"

    if production_path.exists():
        selected_model_path = production_path
    elif baseline_path.exists():
        selected_model_path = baseline_path
    else:
        raise FileNotFoundError("No model artifact found. Run baseline or advanced training first.")

    bundle = joblib.load(selected_model_path)
    threshold = float(bundle.get("threshold", 0.5))

    df = load_cleveland_dataset(RAW_DATA_PATH)
    x, y = get_feature_target(df)

    _, x_test, _, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=SEED,
        stratify=y,
    )

    y_prob = bundle["model"].predict_proba(x_test)[:, 1]
    y_true = y_test.to_numpy()

    _save_roc_curve(y_true, y_prob, REPORT_DIR / "baseline_roc_curve.png")
    _save_pr_curve(y_true, y_prob, REPORT_DIR / "baseline_pr_curve.png")
    _save_confusion_matrix(y_true, y_prob, threshold, REPORT_DIR / "baseline_confusion_matrix.png")
    _save_calibration_curve(y_true, y_prob, REPORT_DIR / "baseline_calibration_curve.png")

    metrics_summary = {
        "model_source": str(selected_model_path),
        "baseline_threshold": threshold,
        "sample_count": int(len(y_true)),
        "positive_rate": float(pd.Series(y_true).mean()),
    }
    (REPORT_DIR / "metrics_summary.json").write_text(json.dumps(metrics_summary, indent=2), encoding="utf-8")

    _write_model_comparison(
        MODEL_DIR / "baseline_metrics.json",
        MODEL_DIR / "deep_metrics.json",
        REPORT_DIR / "model_comparison.md",
    )

    print("Report artifacts created in reports/")


if __name__ == "__main__":
    main()
