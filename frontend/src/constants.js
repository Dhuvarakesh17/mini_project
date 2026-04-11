export const initialForm = {
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

export const fields = Object.keys(initialForm);

export const fieldMeta = {
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

export const fieldConstraints = {
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

export const heartRiskFactors = [
  {
    category: "Blood Pressure",
    factors: [
      {
        name: "High Resting Blood Pressure",
        description:
          "Blood pressure consistently above 130/80 mm Hg increases strain on the heart and arteries",
        risk: "High",
      },
      {
        name: "Normal Blood Pressure",
        description: "Below 120/80 mm Hg is ideal for heart health",
        risk: "Low",
      },
    ],
  },
  {
    category: "Cholesterol Levels",
    factors: [
      {
        name: "High Serum Cholesterol",
        description:
          "Cholesterol above 200 mg/dL increases plaque buildup in arteries",
        risk: "High",
      },
      {
        name: "Low Cholesterol",
        description: "Below 200 mg/dL is generally favorable",
        risk: "Low",
      },
    ],
  },
  {
    category: "Blood Sugar",
    factors: [
      {
        name: "High Fasting Blood Sugar",
        description:
          "Fasting glucose above 120 mg/dL indicates diabetes or prediabetes risk",
        risk: "High",
      },
      {
        name: "Normal Fasting Blood Sugar",
        description: "Below 100 mg/dL is normal",
        risk: "Low",
      },
    ],
  },
  {
    category: "Heart Function",
    factors: [
      {
        name: "Low Maximum Heart Rate",
        description:
          "Inability to achieve normal heart rate during exercise may indicate poor cardiac fitness",
        risk: "High",
      },
      {
        name: "Exercise-Induced Angina",
        description:
          "Chest pain during physical exertion is a warning sign of compromised blood flow",
        risk: "High",
      },
    ],
  },
  {
    category: "ECG & Vessel Health",
    factors: [
      {
        name: "Abnormal Resting ECG",
        description:
          "Electrocardiogram abnormalities indicate electrical or structural heart issues",
        risk: "High",
      },
      {
        name: "Multiple Vessel Disease",
        description:
          "Calcification in 2+ major coronary arteries significantly increases risk",
        risk: "High",
      },
    ],
  },
  {
    category: "Demographic & Lifestyle",
    factors: [
      {
        name: "Advanced Age",
        description: "Risk increases significantly after age 40-50",
        risk: "Moderate",
      },
      {
        name: "Male Gender",
        description:
          "Males generally have higher heart disease risk than premenopausal females",
        risk: "Moderate",
      },
    ],
  },
];

export function parseApiError(details) {
  if (!Array.isArray(details) || details.length === 0) {
    return "Prediction failed due to invalid input.";
  }

  return details
    .map((item) => {
      const field = Array.isArray(item?.loc)
        ? item.loc[item.loc.length - 1]
        : "field";
      const message = item?.msg || "invalid value";
      return `${field}: ${message}`;
    })
    .join("; ");
}

export function buildDetermination(probability, threshold) {
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
