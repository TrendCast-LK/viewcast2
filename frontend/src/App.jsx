import { Routes, Route, Navigate } from "react-router-dom";
import SignIn from "./pages/SignIn";
import SignUp from "./pages/SignUp";
import Dashboard from "./pages/Dashboard";
import NewPrediction from "./pages/NewPrediction";
import PredictionResult from "./pages/PredictionResult";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<SignIn />} />
      <Route path="/sign-up" element={<SignUp />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/new-prediction" element={<NewPrediction />} />
      <Route path="/prediction-result" element={<PredictionResult />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
