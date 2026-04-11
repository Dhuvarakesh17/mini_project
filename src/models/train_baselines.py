from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.data.load_dataset import get_feature_target, load_cleveland_dataset
from src.features.preprocess import build_preprocessor
from src.models.evaluate import classification_report_dict, find_best_threshold


RAW_DATA_PATH = Path("data/raw/processed_cleveland.csv")
MODEL_DIR = Path("models")


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    df = load_cleveland_dataset(RAW_DATA_PATH)
    x, y = get_feature_target(df)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            class_weight="balanced",
            random_state=42,
        ),
    }

    results = {}
    best_name = None
    best_score = -np.inf
    best_bundle = None

    for model_name, estimator in models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                ("classifier", estimator),
            ]
        )

        pipeline.fit(x_train, y_train)
        y_prob = pipeline.predict_proba(x_test)[:, 1]
        threshold = find_best_threshold(y_test.to_numpy(), y_prob)
        metrics = classification_report_dict(y_test.to_numpy(), y_prob, threshold)

        results[model_name] = metrics

        if metrics["roc_auc"] > best_score:
            best_score = metrics["roc_auc"]
            best_name = model_name
            best_bundle = {
                "model": pipeline,
                "threshold": threshold,
                "metrics": metrics,
                "feature_order": list(x.columns),
            }

    if best_bundle is None or best_name is None:
        raise RuntimeError("No model was trained.")

    joblib.dump(best_bundle, MODEL_DIR / "best_baseline.joblib")

    summary = {
        "selected_model": best_name,
        "model_results": results,
    }
    (MODEL_DIR / "baseline_metrics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Training complete.")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
