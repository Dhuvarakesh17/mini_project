import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  initialForm,
  fields,
  fieldMeta,
  fieldHelpText,
  fieldConstraints,
  fieldChoices,
  parseApiError,
  buildDetermination,
} from "../constants";

export default function Dashboard() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const apiBase = useMemo(
    () => import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
    [],
  );

  const updateField = (field, value) => {
    const parsed = value === "" ? "" : Number(value);
    setForm((prev) => ({ ...prev, [field]: parsed }));
  };

  const buildPayload = () =>
    Object.fromEntries(
      Object.entries(form).map(([field, value]) => [field, Number(value)]),
    );

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
        body: JSON.stringify(buildPayload()),
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
        <h2>Patient Risk Prediction Dashboard</h2>
        <p className="subtitle">
          Fill in your health details to get an estimated heart-risk score
        </p>

        <section className="panel">
          <h3>Health Details Form</h3>
          <form onSubmit={onSubmit} className="grid">
            {fields.map((field) => (
              <label key={field}>
                <span>{fieldMeta[field]?.label || field}</span>
                <small className="field-help">{fieldHelpText[field]}</small>
                {fieldChoices[field] ? (
                  <select
                    value={form[field]}
                    onChange={(e) => updateField(field, e.target.value)}
                    required
                  >
                    <option value="">Select an option</option>
                    {fieldChoices[field].map((choice) => (
                      <option key={choice.value} value={choice.value}>
                        {choice.label}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    type="number"
                    value={form[field]}
                    onChange={(e) => updateField(field, e.target.value)}
                    min={fieldConstraints[field]?.min}
                    max={fieldConstraints[field]?.max}
                    step={fieldConstraints[field]?.step}
                    placeholder="Enter value"
                    required
                  />
                )}
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
                {result.risk_label === "high_risk"
                  ? "⚠️ Higher chance of heart problem"
                  : "✓ Lower chance of heart problem"}
              </h3>
              <p>
                <strong>Probability:</strong>{" "}
                {(result.risk_probability * 100).toFixed(2)}%
              </p>
              <p>
                <strong>Threshold:</strong>{" "}
                {(result.threshold * 100).toFixed(2)}%
              </p>
              <p>
                <strong>Model:</strong> {result.model_name}
              </p>
              <p className="result-note">
                Prediction report saved with insights. View it in{" "}
                <Link to="/reports">See Reports</Link>.
              </p>
              <p className="result-note">
                This is a screening estimate, not a final diagnosis.
              </p>

              {determination ? (
                <div className={`determination ${determination.stage}`}>
                  <h4>{determination.title}</h4>
                  <p>{determination.summary}</p>
                </div>
              ) : null}
            </section>
          ) : null}
        </section>
      </main>
    </div>
  );
}
