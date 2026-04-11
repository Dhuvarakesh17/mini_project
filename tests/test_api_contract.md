Manual smoke test checklist

1. Train baseline model:
   python -m src.models.train_baselines

2. Start API:
   uvicorn src.api.main:app --reload

3. Health check:
   GET http://127.0.0.1:8000/health

4. Prediction payload example:
   POST http://127.0.0.1:8000/predict
   {
   "age": 57,
   "sex": 1,
   "cp": 2,
   "trestbps": 130,
   "chol": 236,
   "fbs": 0,
   "restecg": 1,
   "thalach": 174,
   "exang": 0,
   "oldpeak": 0.0,
   "slope": 1,
   "ca": 1,
   "thal": 2
   }
