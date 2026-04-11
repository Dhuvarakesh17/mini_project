import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation";
import Dashboard from "./pages/Dashboard";
import Reports from "./pages/Reports";
import HeartRiskFactors from "./pages/HeartRiskFactors";

export default function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/risk-factors" element={<HeartRiskFactors />} />
      </Routes>
    </BrowserRouter>
  );
}
