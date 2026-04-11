import { heartRiskFactors } from "../constants";

export default function HeartRiskFactors() {
  return (
    <div className="page">
      <main className="card">
        <h2>Heart Disease Risk Factors & Prediction Criteria</h2>
        <p className="subtitle">
          Understanding the key factors that contribute to heart disease risk
          and how our model predicts risk
        </p>

        <section className="panel">
          <h3>What Causes Heart Disease Risk?</h3>
          <p>
            Heart disease is a complex condition influenced by multiple
            physiological, genetic, and lifestyle factors. Our prediction model
            analyzes 13 clinical parameters to assess the likelihood of coronary
            artery disease.
          </p>
        </section>

        <section className="panel">
          <h3>Key Risk Factors</h3>
          <div className="factors-grid">
            {heartRiskFactors.map((category) => (
              <div key={category.category} className="factor-category">
                <h4>{category.category}</h4>
                <div className="factors-list">
                  {category.factors.map((factor) => (
                    <div
                      key={factor.name}
                      className={`factor-item ${factor.risk.toLowerCase()}-risk`}
                    >
                      <div className="factor-header">
                        <h5>{factor.name}</h5>
                        <span className="risk-badge">{factor.risk}</span>
                      </div>
                      <p className="factor-description">{factor.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="panel">
          <h3>How Does the Prediction Model Work?</h3>
          <div className="explanation-grid">
            <article className="explanation-box">
              <h4>📊 13 Clinical Parameters</h4>
              <p>
                The model evaluates patient data across blood pressure,
                cholesterol, blood sugar, heart function, ECG findings, vessel
                health, age, and sex to create a comprehensive risk profile.
              </p>
            </article>

            <article className="explanation-box">
              <h4>🧠 Machine Learning Algorithm</h4>
              <p>
                Advanced deep learning and gradient boosting models are trained
                on historical patient data to identify patterns that distinguish
                high-risk patients from low-risk individuals.
              </p>
            </article>

            <article className="explanation-box">
              <h4>⚠️ Risk Probability Score</h4>
              <p>
                The model outputs a probability score (0-100%) indicating the
                likelihood of coronary artery disease. This score is compared
                against a clinical threshold for risk classification.
              </p>
            </article>

            <article className="explanation-box">
              <h4>🎯 Evidence-Based Thresholds</h4>
              <p>
                Risk categories are determined using clinically validated
                thresholds. Borderline cases are flagged for clinical follow-up
                rather than definitive diagnosis.
              </p>
            </article>

            <article className="explanation-box">
              <h4>📈 Explainability & Transparency</h4>
              <p>
                The model identifies which features most strongly influence each
                prediction, enabling clinicians to understand the reasoning
                behind the assessment.
              </p>
            </article>

            <article className="explanation-box">
              <h4>🔍 Continuous Validation</h4>
              <p>
                Model performance is regularly evaluated on test data. Metrics
                like ROC curves, confusion matrices, and feature importance are
                continuously monitored.
              </p>
            </article>
          </div>
        </section>

        <section className="panel">
          <h3>Risk Classification Criteria</h3>
          <div className="criteria-table">
            <div className="criteria-row header">
              <div className="criteria-col">Risk Level</div>
              <div className="criteria-col">Probability Range</div>
              <div className="criteria-col">Recommendation</div>
            </div>

            <div className="criteria-row severe-risk">
              <div className="criteria-col">
                <strong>Critical Risk</strong>
              </div>
              <div className="criteria-col">80%+</div>
              <div className="criteria-col">
                Urgent cardiology review and intervention
              </div>
            </div>

            <div className="criteria-row moderate-risk">
              <div className="criteria-col">
                <strong>Elevated Risk</strong>
              </div>
              <div className="criteria-col">60-80%</div>
              <div className="criteria-col">
                Close clinical follow-up and targeted interventions
              </div>
            </div>

            <div className="criteria-row watch-risk">
              <div className="criteria-col">
                <strong>Borderline Risk</strong>
              </div>
              <div className="criteria-col">50-60%</div>
              <div className="criteria-col">
                Repeat evaluation and lifestyle modifications
              </div>
            </div>

            <div className="criteria-row watch-risk">
              <div className="criteria-col">
                <strong>Low Current Risk</strong>
              </div>
              <div className="criteria-col">35-50%</div>
              <div className="criteria-col">
                Preventive care and periodic screening
              </div>
            </div>

            <div className="criteria-row low-risk">
              <div className="criteria-col">
                <strong>Low Risk</strong>
              </div>
              <div className="criteria-col">&lt;35%</div>
              <div className="criteria-col">
                Routine health maintenance and annual checkups
              </div>
            </div>
          </div>
        </section>

        <section className="panel">
          <h3>Prevention Strategies</h3>
          <div className="prevention-grid">
            <div className="prevention-item">
              <h4>🏃 Exercise Regularly</h4>
              <p>
                At least 150 minutes of moderate aerobic activity per week helps
                improve cardiovascular fitness and reduce risk.
              </p>
            </div>
            <div className="prevention-item">
              <h4>🥗 Healthy Diet</h4>
              <p>
                Choose heart-healthy foods low in saturated fat, sodium, and
                cholesterol. Emphasize fruits, vegetables, whole grains, and
                lean proteins.
              </p>
            </div>
            <div className="prevention-item">
              <h4>⚖️ Maintain Healthy Weight</h4>
              <p>
                Excess weight increases strain on the heart. A BMI between
                18.5-24.9 is generally considered healthy.
              </p>
            </div>
            <div className="prevention-item">
              <h4>🚭 Don't Smoke</h4>
              <p>
                Smoking damages blood vessels and increases blood pressure.
                Quitting significantly reduces heart disease risk.
              </p>
            </div>
            <div className="prevention-item">
              <h4>💤 Quality Sleep</h4>
              <p>
                7-9 hours of quality sleep per night supports cardiovascular
                health and reduces stress.
              </p>
            </div>
            <div className="prevention-item">
              <h4>🧘 Manage Stress</h4>
              <p>
                Chronic stress elevates blood pressure and heart rate. Practice
                meditation, yoga, or other relaxation techniques.
              </p>
            </div>
          </div>
        </section>

        <section className="panel">
          <h3>When to Seek Medical Attention</h3>
          <div className="warning-box">
            <p>
              <strong>Seek immediate medical care if you experience:</strong>
            </p>
            <ul>
              <li>
                Chest pain or pressure, especially during physical activity
              </li>
              <li>Shortness of breath at rest or with minimal exertion</li>
              <li>Unusual fatigue or weakness</li>
              <li>Irregular heartbeat or heart palpitations</li>
              <li>Persistent swelling in legs, ankles, or feet</li>
              <li>Fainting or severe dizziness</li>
            </ul>
            <p>
              <strong>Note:</strong> This tool provides clinical support, not
              diagnosis. Always consult with a qualified healthcare provider for
              medical decisions.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}
