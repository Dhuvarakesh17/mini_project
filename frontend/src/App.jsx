import { useEffect, useMemo, useState } from "react";

const initialForm = {
  age: 57,
  sex: 1,
  cp: 2,
  trestbps: 130,
  chol: 236,
  fbs: 0,
  restecg: 1,
  thalach: 174,
  exang: 0,
  oldpeak: 0,
  slope: 1,
  ca: 1,
  thal: 2,
};

const fields = Object.keys(initialForm);

const fieldMeta = {
  age: { label: "Age (years)", code: "age" },
  sex: { label: "Sex (0 = female, 1 = male)", code: "sex" },
  cp: { label: "Chest Pain Type", code: "cp" },
  trestbps: { label: "Resting Blood Pressure (mm Hg)", code: "trestbps" },
  chol: { label: "Serum Cholesterol (mg/dL)", code: "chol" },
  fbs: { label: "Fasting Blood Sugar > 120 mg/dL", code: "fbs" },
  restecg: { label: "Resting ECG Result", code: "restecg" },
  thalach: { label: "Maximum Heart Rate Achieved", code: "thalach" },
  exang: { label: "Exercise-Induced Angina", code: "exang" },
  oldpeak: { label: "ST Depression (Oldpeak)", code: "oldpeak" },
  slope: { label: "Slope of Peak Exercise ST Segment", code: "slope" },
  ca: { label: "Number of Major Vessels (0-4)", code: "ca" },
  thal: { label: "Thalassemia Category", code: "thal" },
};

const fieldConstraints = {
  age: { min: 18, max: 120, step: 1 },
  sex: { min: 0, max: 1, step: 1 },
  cp: { min: 0, max: 3, step: 1 },
  trestbps: { min: 70, max: 250, step: 1 },
  chol: { min: 100, max: 700, step: 1 },
  fbs: { min: 0, max: 1, step: 1 },
  restecg: { min: 0, max: 2, step: 1 },
  thalach: { min: 50, max: 250, step: 1 },
  exang: { min: 0, max: 1, step: 1 },
  oldpeak: { min: 0, max: 10, step: 0.1 },
  slope: { min: 0, max: 2, step: 1 },
  ca: { min: 0, max: 4, step: 1 },
  thal: { min: 0, max: 3, step: 1 },
};

function parseApiError(details) {
  if (!Array.isArray(details) || details.length === 0) {
    return "Prediction failed due to invalid input.";
  }

  return details
    .map((item) => {
      const field = Array.isArray(item?.loc) ? item.loc[item.loc.length - 1] : "field";
      const message = item?.msg || "invalid value";
      return `${field}: ${message}`;
    })
    .join("; ");
}

function buildDetermination(probability, threshold) {
  const highRisk = probability >= threshold;

  if (highRisk && probability >= 0.8) {
    return {
      title: "Critical Disease Probability",
      stage: "severe-risk",
      summary: "Strong likelihood of heart disease pattern in current profile.",
      keywords: [
        "high-risk",
        "probable-coronary-disease",
        "urgent-cardiology-review",
        "abnormal-pattern-detected",
      ],
    };
  }

  if (highRisk && probability >= 0.6) {
    return {
      title: "Elevated Disease Probability",
      stage: "moderate-risk",
      summary:
        "Model indicates elevated disease likelihood and follow-up is recommended.",
      keywords: [
        "elevated-risk",
        "possible-cardiac-disease",
        "clinical-follow-up",
        "risk-factor-burden",
      ],
    };
  }

  if (highRisk) {
    return {
      title: "Borderline Positive Screening",
      stage: "watch-risk",
      summary: "Prediction crosses threshold with borderline confidence.",
      keywords: [
        "borderline-positive",
        "repeat-evaluation",
        "preventive-care-path",
        "monitor-trend",
      ],
    };
  }

  if (probability >= 0.35) {
    return {
      title: "Low Current Probability (Watch Zone)",
      stage: "watch-risk",
      summary: "Current risk is below threshold but not negligible.",
      keywords: [
        "sub-threshold-risk",
        "lifestyle-intervention",
        "periodic-screening",
        "monitor-risk-factors",
      ],
    };
  }

  return {
    title: "Low Disease Probability",
    stage: "low-risk",
    summary: "No strong disease signal detected from current feature profile.",
    keywords: [
      "low-risk",
      "no-strong-disease-signal",
      "routine-prevention",
      "annual-checkup",
    ],
  };
}

export default function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [reports, setReports] = useState(null);
  const [reportsLoading, setReportsLoading] = useState(false);
  const [reportsError, setReportsError] = useState("");

  const apiBase = useMemo(
    () => import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
    [],
  );

  const updateField = (field, value) => {
    const parsed = value === "" ? "" : Number(value);
    setForm((prev) => ({ ...prev, [field]: parsed }));
  };

  const loadReports = async () => {
    setReportsLoading(true);
    setReportsError("");
    try {
      const response = await fetch(`${apiBase}/reports/summary`);
      if (!response.ok) {
        throw new Error(`Reports unavailable (${response.status})`);
      }
      const payload = await response.json();
      setReports(payload);
    } catch (err) {
      setReportsError(err.message || "Could not load reports");
    } finally {
      setReportsLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  const onSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${apiBase}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        let message = `Prediction failed (${response.status})`;
        try {
          const errorPayload = await response.json();
          if (response.status === 422 && errorPayload?.detail) {
            message = parseApiError(errorPayload.detail);
          }
        } catch {
          // Keep default fallback message when response body is not JSON.
        }
        throw new Error(message);
      }

      const payload = await response.json();
      setResult(payload);
    } catch (err) {
      setError(err.message || "Unexpected error");
    } finally {
      setLoading(false);
    }
  };

  const determination = result
    ? buildDetermination(result.risk_probability, result.threshold)
    : null;

  return (
    <div className="page">
      <main className="card">
        <h1>Heart Disease Risk Intelligence Dashboard</h1>
        <p className="subtitle">
          Clinical support prototype with prediction, evaluation visuals, and
          explainability highlights.
        </p>

        <section className="panel">
          <h2>Patient Risk Prediction</h2>
          <form onSubmit={onSubmit} className="grid">
            {fields.map((field) => (
              <label key={field}>
                <span>{fieldMeta[field]?.label || field}</span>
                <small className="field-code">
                  Code: {fieldMeta[field]?.code || field}
                </small>
                <input
                  type="number"
                  value={form[field]}
                  onChange={(e) => updateField(field, e.target.value)}
                  min={fieldConstraints[field]?.min}
                  max={fieldConstraints[field]?.max}
                  step={fieldConstraints[field]?.step}
                  required
                />
              </label>
            ))}

            <button type="submit" disabled={loading}>
              {loading ? "Predicting..." : "Predict Risk"}
            </button>
          </form>

          {error ? <p className="error">{error}</p> : null}

          {result ? (
            <section className="result">
              <h3>
                {result.risk_label === "high_risk" ? "High Risk" : "Low Risk"}
              </h3>
              <p>Probability: {(result.risk_probability * 100).toFixed(2)}%</p>
              <p>Threshold: {(result.threshold * 100).toFixed(2)}%</p>
              <p>Model: {result.model_name}</p>

              {determination ? (
                <div className={`determination ${determination.stage}`}>
                  <h4>{determination.title}</h4>
                  <p>{determination.summary}</p>
                  <div className="keyword-wrap">
                    {determination.keywords.map((keyword) => (
                      <span key={keyword} className="keyword-pill">
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              ) : null}
            </section>
          ) : null}
        </section>

        <section className="panel">
          <div className="panel-head">
            <h2>Model Reports and Visuals</h2>
            <button
              type="button"
              onClick={loadReports}
              disabled={reportsLoading}
            >
              {reportsLoading ? "Refreshing..." : "Refresh Reports"}
            </button>
          </div>

          {reportsError ? <p className="error">{reportsError}</p> : null}

          {reports ? (
            <>
              <div className="stats-grid">
                <article className="stat-box">
                  <h3>Test Samples</h3>
                  <p>{reports.metrics_summary?.sample_count ?? "-"}</p>
                </article>
                <article className="stat-box">
                  <h3>Positive Rate</h3>
                  <p>
                    {reports.metrics_summary?.positive_rate != null
                      ? `${(reports.metrics_summary.positive_rate * 100).toFixed(2)}%`
                      : "-"}
                  </p>
                </article>
                <article className="stat-box">
                  <h3>Threshold</h3>
                  <p>
                    {reports.metrics_summary?.baseline_threshold != null
                      ? reports.metrics_summary.baseline_threshold.toFixed(2)
                      : "-"}
                  </p>
                </article>
              </div>

              <div className="image-grid">
                {reports.available_images?.map((imageName) => (
                  <figure key={imageName} className="chart-card">
                    <img
                      src={`${apiBase}/reports-assets/${imageName}`}
                      alt={imageName}
                    />
                    <figcaption>{imageName.replaceAll("_", " ")}</figcaption>
                  </figure>
                ))}
              </div>

              <div className="bottom-grid">
                <article className="result">
                  <h3>Top Feature Signals</h3>
                  {reports.top_features?.length ? (
                    <ul className="feature-list">
                      {reports.top_features.map((item) => (
                        <li key={item.feature}>
                          <span>{item.feature}</span>
                          <strong>
                            {Number(item.importance_mean).toFixed(4)}
                          </strong>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No feature importance data available.</p>
                  )}
                </article>

                <article className="result">
                  <h3>Model Comparison</h3>
                  <pre>
                    {reports.model_comparison_markdown ||
                      "No comparison report found."}
                  </pre>
                </article>
              </div>
            </>
          ) : null}
        </section>
      </main>
    </div>
  );
}
