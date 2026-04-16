export const initialForm = {
  age: "",
  sex: "",
  cp: "",
  trestbps: "",
  chol: "",
  fbs: "",
  restecg: "",
  thalach: "",
  exang: "",
  oldpeak: "",
  slope: "",
  ca: "",
  thal: "",
};

export const fields = Object.keys(initialForm);

export const fieldMeta = {
  age: { label: "Your age", code: "age" },
  sex: { label: "Sex", code: "sex" },
  cp: { label: "Type of chest discomfort", code: "cp" },
  trestbps: { label: "Resting blood pressure (mm Hg)", code: "trestbps" },
  chol: { label: "Cholesterol (mg/dL)", code: "chol" },
  fbs: { label: "Fasting blood sugar", code: "fbs" },
  restecg: { label: "Heart test result (ECG)", code: "restecg" },
  thalach: { label: "Highest heart rate during activity", code: "thalach" },
  exang: { label: "Chest pain during exercise", code: "exang" },
  oldpeak: { label: "Exercise stress value (Oldpeak)", code: "oldpeak" },
  slope: { label: "ECG trend during exercise", code: "slope" },
  ca: { label: "Blocked major vessels (scan result)", code: "ca" },
  thal: { label: "Blood flow test result", code: "thal" },
};

export const fieldHelpText = {
  age: "Enter age in years.",
  sex: "Select sex listed in your health record.",
  cp: "Choose the option that best matches your symptom pattern.",
  trestbps: "Use your recent resting blood pressure value.",
  chol: "Use your latest cholesterol lab result.",
  fbs: "Choose based on your fasting sugar test.",
  restecg: "Use the summary from your ECG report.",
  thalach: "Use your highest measured heart rate during activity.",
  exang: "Did chest pain happen during physical activity?",
  oldpeak: "Use this only if available in your stress test report.",
  slope: "Use your stress ECG report if available.",
  ca: "Number of blocked vessels from scan/angiography report.",
  thal: "Select the blood flow/perfusion report result.",
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

export const fieldChoices = {
  sex: [
    { value: 0, label: "Female" },
    { value: 1, label: "Male" },
  ],
  cp: [
    { value: 0, label: "Typical chest pain" },
    { value: 1, label: "Atypical chest pain" },
    { value: 2, label: "Chest pain likely not heart-related" },
    { value: 3, label: "No chest pain symptoms" },
  ],
  fbs: [
    { value: 0, label: "120 mg/dL or below" },
    { value: 1, label: "Above 120 mg/dL" },
  ],
  restecg: [
    { value: 0, label: "Normal ECG" },
    { value: 1, label: "Minor ECG change" },
    { value: 2, label: "Major ECG change" },
  ],
  exang: [
    { value: 0, label: "No" },
    { value: 1, label: "Yes" },
  ],
  slope: [
    { value: 0, label: "Upward trend" },
    { value: 1, label: "Flat trend" },
    { value: 2, label: "Downward trend" },
  ],
  ca: [
    { value: 0, label: "0 blocked vessels" },
    { value: 1, label: "1 blocked vessel" },
    { value: 2, label: "2 blocked vessels" },
    { value: 3, label: "3 blocked vessels" },
    { value: 4, label: "4 blocked vessels" },
  ],
  thal: [
    { value: 0, label: "Unknown / not sure" },
    { value: 1, label: "Normal blood flow" },
    { value: 2, label: "Fixed blood flow issue" },
    { value: 3, label: "Stress-related blood flow issue" },
  ],
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
