# Heart Disease Risk Intelligence - Multi-Page Website

## Overview

The frontend has been restructured into a **three-page website** with navigation, built using **React Router v6**.

---

## Pages

### 1. **Dashboard** (`/`)

- **Purpose**: Patient risk prediction interface
- **Features**:
  - Input form with 13 clinical parameters
  - Real-time prediction submission
  - Risk classification display
  - Risk determination with keywords
  - **File**: `src/pages/Dashboard.jsx`

### 2. **Reports** (`/reports`)

- **Purpose**: Model performance evaluation and visualization
- **Features**:
  - Performance metrics (sample count, positive rate, threshold)
  - Evaluation visualizations (confusion matrix, ROC curve, PR curve, calibration curve)
  - Top feature importance signals
  - Model comparison report
  - Refresh controls
  - **File**: `src/pages/Reports.jsx`

### 3. **Heart Risk Factors** (`/risk-factors`)

- **Purpose**: Educational content about heart disease causes and prediction criteria
- **Features**:
  - What Causes Heart Disease Risk (overview)
  - 6 Key Risk Factor Categories:
    - Blood Pressure
    - Cholesterol Levels
    - Blood Sugar
    - Heart Function
    - ECG & Vessel Health
    - Demographic & Lifestyle
  - How the Prediction Model Works (6 components)
  - Risk Classification Criteria (5 levels from critical to low)
  - Prevention Strategies (6 key strategies)
  - When to Seek Medical Attention (warning signs)
  - **File**: `src/pages/HeartRiskFactors.jsx`

---

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx                      # Main app with Router setup
│   ├── main.jsx                     # React entry point
│   ├── constants.js                 # Shared constants & utilities
│   ├── styles.css                   # Global styles (updated)
│   ├── components/
│   │   └── Navigation.jsx           # Top navigation bar
│   └── pages/
│       ├── Dashboard.jsx            # Prediction form page
│       ├── Reports.jsx              # Reports & metrics page
│       └── HeartRiskFactors.jsx     # Educational content page
├── index.html
├── package.json                     # Updated with react-router-dom
└── vite.config.js
```

---

## Key Changes

### Dependencies Added

- `react-router-dom@^6.20.0` - Client-side routing

### Files Created

1. **src/constants.js** - Extracted shared utilities:
   - Form constants (initialForm, fields, fieldMeta, fieldConstraints)
   - Heart risk factors data
   - `parseApiError()` function
   - `buildDetermination()` function

2. **src/components/Navigation.jsx** - Sticky navigation bar with:
   - Logo (with heart emoji)
   - Three main navigation links
   - Active state styling
   - Mobile-responsive design

3. **src/pages/Dashboard.jsx** - Dashboard page component
   - Moved prediction form logic from App.jsx
   - Maintains all original functionality
   - Clean separation of concerns

4. **src/pages/Reports.jsx** - Reports page component
   - Moved reports logic from App.jsx
   - Displays model performance metrics
   - Gallery of evaluation visualizations
   - Feature importance and model comparison

5. **src/pages/HeartRiskFactors.jsx** - New educational page
   - 6 risk factor categories with detailed descriptions
   - Model explanation section
   - 5-level risk classification system
   - Prevention strategies guide
   - Medical emergency guidance

### Files Modified

1. **App.jsx** - Refactored to use React Router
   - Now only contains BrowserRouter, Routes, and Route imports
   - Cleaner, more maintainable structure

2. **styles.css** - Enhanced with:
   - Navigation bar styling (sticky, gradient background, responsive)
   - Risk factor categories styling
   - Explanation boxes with hover effects
   - Criteria table with risk-level color coding
   - Prevention strategies grid
   - Warning box styling
   - All new page component styles

3. **package.json** - Added react-router-dom dependency

---

## Navigation Features

- **Sticky Navigation**: Always visible at top
- **Active Link Highlighting**: Shows current page
- **Color-Coded Design**: Maintains brand colors
- **Responsive Layout**: Works on mobile and desktop
- **Brand Logo**: ❤️ Heart Risk Intelligence

---

## Styling Improvements

### Color Scheme

- Navigation: Dark blue gradient (#2c3e50, #34495e)
- Accent: Warm brown (#b64d2e)
- Risk Levels:
  - **Severe**: #fff0ec (light red)
  - **Moderate**: #fff6ea (light orange)
  - **Watch**: #f9f6ef (light beige)
  - **Low**: #f1f7ee (light green)

### Responsive Design

- Grid-based layouts with `auto-fit` and `minmax`
- Mobile-first approach
- Flexible navigation that adapts to screen size

---

## Running the Application

### Development

```bash
cd frontend
npm run dev
```

### Build

```bash
npm run build
```

### Preview

```bash
npm run preview
```

---

## Integration with Backend

All three pages integrate with the backend API:

- **Dashboard**: Uses `/predict` endpoint
- **Reports**: Uses `/reports/summary` and `/reports-assets/` endpoints
- **Heart Risk Factors**: Educational/static content (no API calls)

### Environment Configuration

Set `VITE_API_BASE_URL` in your `.env` or environment to point to your backend:

```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

## Future Enhancements

1. Add patient history/records management
2. Export prediction reports as PDF
3. Add data visualization dashboard
4. Implement user authentication
5. Add multilingual support
6. Create mobile app version
