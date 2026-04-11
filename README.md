# Heart Disease Risk Prediction (Classification Models)

This project implements an end-to-end heart disease risk prediction workflow using:

- Baseline ML models (Logistic Regression, Random Forest)
- Advanced ensemble benchmarking pipeline with CV-based model selection
- Deep learning model (PyTorch)
- FastAPI inference service
- React frontend (Vite)

## 1. Python Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Train Models

Train baseline and save deployment artifact:

```bash
python -m src.models.train_baselines
```

Train advanced production pipeline (recommended):

```bash
python -m src.models.train_advanced
```

Train advanced pipeline with your own dataset:

```bash
python -m src.models.train_advanced --data-path data/raw/your_dataset.csv
```

This command benchmarks multiple stronger models, tunes threshold on validation data,
and writes the production artifact to `models/best_production.joblib`.

Custom dataset requirements:

- Must include all model features plus target.
- Canonical feature keys: `age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal`.
- Supported aliases (examples): `chest_pain_type -> cp`, `resting_blood_pressure -> trestbps`,
  `fasting_blood_sugar -> fbs`, `resting_ecg -> restecg`, `max_heart_rate -> thalach`.
- Target aliases supported: `target`, `num`, `heart_disease`, `diagnosis`, `label`, `output`.
- Target is binarized automatically: values `> 0` are treated as positive class.

Train deep model artifact:

```bash
python -m src.models.train_deep
```

Generate evaluation reports and charts:

```bash
python -m src.models.generate_reports
```

Generate explainability artifacts (permutation importance + SHAP when available):

```bash
python -m src.models.explain
```

## 3. Start API

```bash
uvicorn src.api.main:app --reload
```

Endpoints:

- `GET /health`
- `POST /predict`

## 4. Start React Frontend

```bash
cd frontend
npm install
npm run dev
```

Optional API URL override:

- set `VITE_API_BASE_URL=http://127.0.0.1:8000`

## 5. Notes

- Dataset source: UCI Cleveland heart disease data.
- Target is binarized: `target > 0` becomes positive class.
- Threshold is tuned on holdout set for baseline model artifact.
- API auto-load priority: `models/best_production.joblib`, then fallback to `models/best_baseline.joblib`.
- This is a decision-support prototype, not a clinical diagnostic system.
