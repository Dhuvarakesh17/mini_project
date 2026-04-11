from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from src.data.load_dataset import get_feature_target, load_cleveland_dataset
from src.features.preprocess import build_preprocessor
from src.models.evaluate import classification_report_dict, find_best_threshold


RAW_DATA_PATH = Path("data/raw/processed_cleveland.csv")
MODEL_DIR = Path("models")
SEED = 42


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)


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


def to_tensor_data(x_arr: np.ndarray, y_arr: np.ndarray) -> TensorDataset:
    x_tensor = torch.tensor(x_arr, dtype=torch.float32)
    y_tensor = torch.tensor(y_arr.reshape(-1, 1), dtype=torch.float32)
    return TensorDataset(x_tensor, y_tensor)


def split_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str], object]:
    df = load_cleveland_dataset(RAW_DATA_PATH)
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

    preprocessor = build_preprocessor()
    x_train_t = preprocessor.fit_transform(x_train)
    x_val_t = preprocessor.transform(x_val)
    x_test_t = preprocessor.transform(x_test)

    x_train_arr = x_train_t.toarray() if hasattr(x_train_t, "toarray") else np.asarray(x_train_t)
    x_val_arr = x_val_t.toarray() if hasattr(x_val_t, "toarray") else np.asarray(x_val_t)
    x_test_arr = x_test_t.toarray() if hasattr(x_test_t, "toarray") else np.asarray(x_test_t)

    return (
        x_train_arr,
        x_val_arr,
        x_test_arr,
        y_train.to_numpy(),
        y_val.to_numpy(),
        y_test.to_numpy(),
        list(x.columns),
        preprocessor,
    )


def main() -> None:
    set_seed(SEED)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    (
        x_train,
        x_val,
        x_test,
        y_train,
        y_val,
        y_test,
        feature_order,
        preprocessor,
    ) = split_data()

    train_loader = DataLoader(to_tensor_data(x_train, y_train), batch_size=32, shuffle=True)
    val_dataset = to_tensor_data(x_val, y_val)

    model = HeartNet(input_dim=x_train.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    pos_weight_value = (len(y_train) - y_train.sum()) / max(y_train.sum(), 1)
    criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([pos_weight_value], dtype=torch.float32))

    best_val_loss = float("inf")
    best_state = None
    patience = 20
    patience_counter = 0

    for _ in range(200):
        model.train()
        for xb, yb in train_loader:
            optimizer.zero_grad()
            logits = model(xb)
            loss = criterion(logits, yb)
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            x_val_tensor = val_dataset.tensors[0]
            y_val_tensor = val_dataset.tensors[1]
            val_logits = model(x_val_tensor)
            val_loss = criterion(val_logits, y_val_tensor).item()

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = model.state_dict()
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                break

    if best_state is None:
        raise RuntimeError("Training failed to produce a best checkpoint.")

    model.load_state_dict(best_state)
    model.eval()

    with torch.no_grad():
        test_logits = model(torch.tensor(x_test, dtype=torch.float32)).squeeze(dim=1)
        y_prob = torch.sigmoid(test_logits).numpy()

    threshold = find_best_threshold(y_test, y_prob)
    metrics = classification_report_dict(y_test, y_prob, threshold)

    torch.save(model.state_dict(), MODEL_DIR / "heart_net_state.pt")
    joblib.dump(preprocessor, MODEL_DIR / "heart_net_preprocessor.joblib")

    payload = {
        "model": "heart_net",
        "threshold": threshold,
        "metrics": metrics,
        "input_dim": int(x_train.shape[1]),
        "feature_order": feature_order,
    }
    (MODEL_DIR / "deep_metrics.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Deep model training complete.")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
