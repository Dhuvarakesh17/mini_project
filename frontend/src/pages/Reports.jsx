import { useEffect, useMemo, useState } from "react";

export default function Reports() {
  const [reports, setReports] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const apiBase = useMemo(
    () => import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
    [],
  );

  const loadReports = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${apiBase}/reports/summary`);
      if (!response.ok) {
        throw new Error(`Reports unavailable (${response.status})`);
      }
      const payload = await response.json();
      setReports(payload);
    } catch (err) {
      setError(err.message || "Could not load reports");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  return (
    <div className="page">
      <main className="card">
        <h2>Model Reports & Performance Visuals</h2>
        <p className="subtitle">
          Comprehensive model evaluation, metrics, feature importance, and
          performance comparisons
        </p>

        <section className="panel">
          <div className="panel-head">
            <h3>Performance Metrics</h3>
            <button type="button" onClick={loadReports} disabled={loading}>
              {loading ? "Refreshing..." : "Refresh Reports"}
            </button>
          </div>

          {error && <p className="error">{error}</p>}

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

              {reports.available_images?.length > 0 && (
                <div className="image-grid">
                  <h3 style={{ gridColumn: "1 / -1", marginTop: "1.5rem" }}>
                    Evaluation Visualizations
                  </h3>
                  {reports.available_images.map((imageName) => (
                    <figure key={imageName} className="chart-card">
                      <img
                        src={`${apiBase}/reports-assets/${imageName}`}
                        alt={imageName}
                      />
                      <figcaption>{imageName.replaceAll("_", " ")}</figcaption>
                    </figure>
                  ))}
                </div>
              )}

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
          ) : (
            !error && <p>Loading reports...</p>
          )}
        </section>
      </main>
    </div>
  );
}
