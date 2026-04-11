from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

from src.data.load_dataset import get_feature_target, load_cleveland_dataset


RAW_DATA_PATH = Path("data/raw/processed_cleveland.csv")
PRODUCTION_MODEL_PATH = Path("models/best_production.joblib")
BASELINE_MODEL_PATH = Path("models/best_baseline.joblib")
REPORT_DIR = Path("reports")
SEED = 42


def _save_permutation_importance(model_bundle: dict, x_test: pd.DataFrame, y_test: pd.Series) -> None:
    model = model_bundle["model"]

    perm = permutation_importance(
        model,
        x_test,
        y_test,
        n_repeats=30,
        random_state=SEED,
        scoring="roc_auc",
    )

    importance_df = pd.DataFrame(
        {
            "feature": x_test.columns,
            "importance_mean": perm.importances_mean,
            "importance_std": perm.importances_std,
        }
    ).sort_values("importance_mean", ascending=False)

    (REPORT_DIR / "feature_importance_permutation.json").write_text(
        importance_df.to_json(orient="records", indent=2),
        encoding="utf-8",
    )

    top = importance_df.head(10).iloc[::-1]
    plt.figure(figsize=(8, 5))
    plt.barh(top["feature"], top["importance_mean"], xerr=top["importance_std"], color="#b64d2e")
    plt.xlabel("Permutation Importance (ROC-AUC decrease)")
    plt.title("Top 10 Baseline Feature Importances")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "feature_importance_permutation.png", dpi=140)
    plt.close()


def _try_save_shap_artifacts(model_bundle: dict, x_train: pd.DataFrame, x_test: pd.DataFrame) -> str:
    try:
        import shap  # type: ignore
    except Exception:
        return "SHAP not available. Install shap to generate SHAP artifacts."

    model = model_bundle["model"]

    # Keep SHAP computation light for quick iteration.
    background = x_train.sample(min(120, len(x_train)), random_state=SEED)
    explain_rows = x_test.sample(min(60, len(x_test)), random_state=SEED)

    try:
        explainer = shap.Explainer(model.predict_proba, background)
        shap_values = explainer(explain_rows)
    except Exception as exc:
        return f"SHAP failed: {exc}"

    try:
        plt.figure()
        shap.plots.beeswarm(shap_values[:, :, 1], show=False, max_display=12)
        plt.tight_layout()
        plt.savefig(REPORT_DIR / "shap_beeswarm.png", dpi=140, bbox_inches="tight")
        plt.close()

        plt.figure()
        shap.plots.waterfall(shap_values[0, :, 1], show=False, max_display=12)
        plt.tight_layout()
        plt.savefig(REPORT_DIR / "shap_waterfall_sample0.png", dpi=140, bbox_inches="tight")
        plt.close()
    except Exception as exc:
        return f"SHAP plots failed: {exc}"

    return "SHAP artifacts created."


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if PRODUCTION_MODEL_PATH.exists():
        model_path = PRODUCTION_MODEL_PATH
    elif BASELINE_MODEL_PATH.exists():
        model_path = BASELINE_MODEL_PATH
    else:
        raise FileNotFoundError("No model artifact found. Run baseline or advanced training first.")

    bundle = joblib.load(model_path)

    df = load_cleveland_dataset(RAW_DATA_PATH)
    x, y = get_feature_target(df)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=SEED,
        stratify=y,
    )

    _save_permutation_importance(bundle, x_test, y_test)
    shap_status = _try_save_shap_artifacts(bundle, x_train, x_test)

    summary = {
        "explainability": {
            "model_source": str(model_path),
            "permutation_json": "reports/feature_importance_permutation.json",
            "permutation_plot": "reports/feature_importance_permutation.png",
            "shap_status": shap_status,
            "shap_beeswarm": "reports/shap_beeswarm.png",
            "shap_waterfall": "reports/shap_waterfall_sample0.png",
        }
    }
    (REPORT_DIR / "explainability_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Explainability artifacts created in reports/")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
