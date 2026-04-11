from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from src.data.load_dataset import get_feature_target, load_cleveland_dataset
from src.features.preprocess import build_preprocessor
from src.models.evaluate import classification_report_dict, find_best_threshold


RAW_DATA_PATH = Path("data/raw/processed_cleveland.csv")
MODEL_DIR = Path("models")
SEED = 42


def _candidate_estimators() -> dict[str, object]:
    return {
        "logistic_regression": LogisticRegression(max_iter=2500, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=500,
            max_depth=10,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=SEED,
        ),
        "extra_trees": ExtraTreesClassifier(
            n_estimators=600,
            max_depth=12,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=SEED,
        ),
        "gradient_boosting": GradientBoostingClassifier(random_state=SEED),
        "svm_rbf": SVC(C=1.2, kernel="rbf", gamma="scale", class_weight="balanced", probability=True),
    }


def _selection_score(metrics: dict[str, float]) -> float:
    # Clinical preference: prioritize sensitivity while keeping discrimination quality.
    return (0.7 * metrics["recall"]) + (0.3 * metrics["roc_auc"])


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train advanced heart disease classifiers.")
    parser.add_argument(
        "--data-path",
        type=str,
        default=str(RAW_DATA_PATH),
        help="Path to input CSV dataset.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    dataset_path = Path(args.data_path)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    df = load_cleveland_dataset(dataset_path)
    x, y = get_feature_target(df)

    x_train_val, x_test, y_train_val, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=SEED,
        stratify=y,
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train_val,
        y_train_val,
        test_size=0.2,
        random_state=SEED,
        stratify=y_train_val,
    )

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

    registry: dict[str, dict] = {}
    best_name = None
    best_threshold = 0.5
    best_estimator = None
    best_score = -np.inf

    for model_name, estimator in _candidate_estimators().items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                ("classifier", estimator),
            ]
        )

        cv_auc = cross_val_score(pipeline, x_train, y_train, scoring="roc_auc", cv=skf, n_jobs=-1)
        pipeline.fit(x_train, y_train)

        val_prob = pipeline.predict_proba(x_val)[:, 1]
        tuned_threshold = find_best_threshold(y_val.to_numpy(), val_prob)
        val_metrics = classification_report_dict(y_val.to_numpy(), val_prob, tuned_threshold)

        test_prob = pipeline.predict_proba(x_test)[:, 1]
        test_metrics = classification_report_dict(y_test.to_numpy(), test_prob, tuned_threshold)

        selection_score = _selection_score(val_metrics)

        registry[model_name] = {
            "cv_roc_auc_mean": float(np.mean(cv_auc)),
            "cv_roc_auc_std": float(np.std(cv_auc)),
            "threshold": float(tuned_threshold),
            "selection_score": float(selection_score),
            "val_metrics": val_metrics,
            "test_metrics": test_metrics,
        }

        if selection_score > best_score:
            best_score = selection_score
            best_name = model_name
            best_threshold = float(tuned_threshold)
            best_estimator = estimator

    if best_name is None or best_estimator is None:
        raise RuntimeError("No model candidates were successfully trained.")

    # Refit the winning model on the full non-test data.
    production_pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("classifier", best_estimator),
        ]
    )
    production_pipeline.fit(x_train_val, y_train_val)

    production_test_prob = production_pipeline.predict_proba(x_test)[:, 1]
    production_test_metrics = classification_report_dict(y_test.to_numpy(), production_test_prob, best_threshold)

    production_bundle = {
        "model": production_pipeline,
        "threshold": best_threshold,
        "metrics": production_test_metrics,
        "selected_model": best_name,
        "selection_policy": "0.7*recall + 0.3*roc_auc on validation split",
        "feature_order": list(x.columns),
        "dataset_path": str(dataset_path),
    }
    joblib.dump(production_bundle, MODEL_DIR / "best_production.joblib")

    payload = {
        "selected_model": best_name,
        "dataset_path": str(dataset_path),
        "selection_policy": production_bundle["selection_policy"],
        "selected_threshold": best_threshold,
        "selected_test_metrics": production_test_metrics,
        "model_registry": registry,
    }
    (MODEL_DIR / "production_metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (MODEL_DIR / "model_registry.json").write_text(json.dumps(registry, indent=2), encoding="utf-8")

    print("Advanced training complete.")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
