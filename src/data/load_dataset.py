from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd


COLUMN_NAMES = [
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
    "target",
]

UCI_CLEVELAND_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/"
    "processed.cleveland.data"
)

FEATURE_COLUMNS = COLUMN_NAMES[:-1]

TARGET_ALIASES = {
    "target",
    "num",
    "heart_disease",
    "heartdisease",
    "diagnosis",
    "label",
    "output",
}

COLUMN_ALIASES = {
    "age": "age",
    "sex": "sex",
    "cp": "cp",
    "chest_pain_type": "cp",
    "trestbps": "trestbps",
    "resting_blood_pressure": "trestbps",
    "chol": "chol",
    "serum_cholesterol": "chol",
    "fbs": "fbs",
    "fasting_blood_sugar": "fbs",
    "restecg": "restecg",
    "resting_ecg": "restecg",
    "thalach": "thalach",
    "max_heart_rate": "thalach",
    "exang": "exang",
    "exercise_induced_angina": "exang",
    "oldpeak": "oldpeak",
    "st_depression": "oldpeak",
    "slope": "slope",
    "ca": "ca",
    "num_major_vessels": "ca",
    "thal": "thal",
}


def _normalize_col_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_").replace("/", "_")


def _canonicalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {}
    for column in df.columns:
        key = _normalize_col_name(column)
        if key in TARGET_ALIASES:
            rename_map[column] = "target"
        elif key in COLUMN_ALIASES:
            rename_map[column] = COLUMN_ALIASES[key]
        else:
            rename_map[column] = key
    return df.rename(columns=rename_map)


def _validate_required_columns(df: pd.DataFrame) -> None:
    missing = [col for col in FEATURE_COLUMNS + ["target"] if col not in df.columns]
    if missing:
        raise ValueError(
            "Dataset is missing required columns: "
            + ", ".join(missing)
            + ". Supported aliases include full clinical names such as chest_pain_type, resting_blood_pressure, and fasting_blood_sugar."
        )


def load_cleveland_dataset(raw_csv_path: str | Path) -> pd.DataFrame:
    """Load dataset from path (or fetch Cleveland default) and normalize schema/target."""
    raw_csv_path = Path(raw_csv_path)
    raw_csv_path.parent.mkdir(parents=True, exist_ok=True)

    if raw_csv_path.exists():
        df = pd.read_csv(raw_csv_path, na_values="?")
    else:
        if raw_csv_path.name != "processed_cleveland.csv":
            raise FileNotFoundError(
                f"Dataset file not found: {raw_csv_path}. Provide a valid CSV path or use data/raw/processed_cleveland.csv"
            )
        df = pd.read_csv(
            UCI_CLEVELAND_URL,
            names=COLUMN_NAMES,
            na_values="?",
        )
        df.to_csv(raw_csv_path, index=False)

    if len(df.columns) == len(COLUMN_NAMES) and not set(COLUMN_NAMES).issubset(df.columns):
        df.columns = COLUMN_NAMES

    df = _canonicalize_columns(df)
    _validate_required_columns(df)

    # Keep only required model columns in a stable order.
    df = df[FEATURE_COLUMNS + ["target"]].copy()

    df["target"] = (pd.to_numeric(df["target"], errors="coerce") > 0).astype(int)

    # Coerce numeric fields to avoid mixed dtypes from missing tokens.
    for col in FEATURE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def get_feature_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    features = df.drop(columns=["target"])
    target = df["target"]
    return features, target
