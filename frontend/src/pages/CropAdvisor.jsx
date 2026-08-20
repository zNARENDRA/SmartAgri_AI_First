import React, { useState, useEffect } from "react";
import { useFarmer } from "../context/FarmerContext";
import { predictCrop, getCropMetrics } from "../services/api";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell
} from "recharts";
import {
  Sprout,
  Sparkles,
  RefreshCw,
  Info,
  CheckCircle2,
  Droplets,
  Clock,
  ShieldAlert,
  BarChart3,
  Sliders
} from "lucide-react";

export default function CropAdvisor() {
  const { profile } = useFarmer();

  const [form, setForm] = useState({
    N: profile.nitrogen || 80,
    P: profile.phosphorus || 45,
    K: profile.potassium || 40,
    temperature: 26.0,
    humidity: 70.0,
    ph: profile.soil_ph || 6.5,
    rainfall: 120.0,
    top_k: 3
  });

  const [result, setResult] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    try {
      const res = await predictCrop({
        N: Number(form.N),
        P: Number(form.P),
        K: Number(form.K),
        temperature: Number(form.temperature),
        humidity: Number(form.humidity),
        ph: Number(form.ph),
        rainfall: Number(form.rainfall),
        top_k: Number(form.top_k)
      });
      setResult(res);
    } catch (err) {
      console.error("Prediction error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handlePredict();
    getCropMetrics().then(setMetrics).catch(() => {});
  }, []);

  const syncProfile = () => {
    setForm((prev) => ({
      ...prev,
      N: profile.nitrogen,
      P: profile.phosphorus,
      K: profile.potassium,
      ph: profile.soil_ph
    }));
  };

  const fetchRealtimeClimate = async () => {
    try {
      const { getCurrentWeather } = await import("../services/api");
      const data = await getCurrentWeather(profile.district || profile.state || "Nashik");
      if (data && data.temperature_celsius !== undefined) {
        setForm((prev) => ({
          ...prev,
          temperature: Math.round(data.temperature_celsius * 10) / 10,
          humidity: Math.round(data.humidity_percentage)
        }));
      }
    } catch (err) {
      console.error("Realtime weather sync error:", err);
    }
  };

  const chartData = result && result.feature_importances ? Object.entries(result.feature_importances).map(([k, v]) => ({
    feature: k === "ph" ? "Soil pH" : k === "temperature" ? "Temp (°C)" : k === "rainfall" ? "Rain (mm)" : k === "humidity" ? "Humidity" : `Nutrient ${k}`,
    importance: Number((v * 100).toFixed(1))
  })).sort((a, b) => b.importance - a.importance) : [];

  return (
    <div className="page-wrapper">
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "20px", flexWrap: "wrap", gap: "12px" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
            <span className="badge badge-green">AI Crop Recommendation</span>
            <span style={{ fontSize: "12px", color: "#64748b", fontWeight: 600 }}>Soil & Agronomic Intelligence</span>
          </div>
          <h1 style={{ fontSize: "24px", fontWeight: 800, color: "#0f172a", letterSpacing: "-0.02em", margin: 0 }}>
            AI Crop Recommendation Engine
          </h1>
          <p style={{ fontSize: "13px", color: "#64748b", marginTop: "2px" }}>
            Identify suitable crops for your exact soil nutrient balance (N-P-K), pH, and climate.
          </p>
        </div>

        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
          <button 
            onClick={fetchRealtimeClimate}
            className="btn btn-secondary"
            style={{ fontSize: "12px", padding: "8px 14px" }}
          >
            <Sparkles size={14} color="#0284c7" /> Live Weather Sync
          </button>
          <button 
            onClick={syncProfile}
            className="btn btn-secondary"
            style={{ fontSize: "12px", padding: "8px 14px" }}
          >
            <RefreshCw size={14} /> Sync from Profile
          </button>
        </div>
      </div>

      <div className="grid-2">
        {/* Left Column: Soil & Climate Input Form */}
        <div className="card">
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "16px", borderBottom: "1px solid #f1f5f9", paddingBottom: "10px" }}>
            <Sliders size={18} color="#059669" />
            <h2 style={{ fontSize: "15px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
              Soil & Climate Parameters
            </h2>
          </div>

          <form onSubmit={handlePredict}>
            {/* Nitrogen (N) */}
            <div className="form-group">
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                <label className="form-label" style={{ margin: 0 }}>Nitrogen (N)</label>
                <span style={{ fontSize: "13px", fontWeight: 700, color: "#059669" }}>{form.N} kg/ha</span>
              </div>
              <input
                type="range"
                min="0"
                max="160"
                value={form.N}
                onChange={(e) => setForm({ ...form, N: Number(e.target.value) })}
                className="slider-range"
              />
            </div>

            {/* Phosphorus (P) */}
            <div className="form-group">
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                <label className="form-label" style={{ margin: 0 }}>Phosphorus (P)</label>
                <span style={{ fontSize: "13px", fontWeight: 700, color: "#0284c7" }}>{form.P} kg/ha</span>
              </div>
              <input
                type="range"
                min="5"
                max="150"
                value={form.P}
                onChange={(e) => setForm({ ...form, P: Number(e.target.value) })}
                className="slider-range"
              />
            </div>

            {/* Potassium (K) */}
            <div className="form-group">
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                <label className="form-label" style={{ margin: 0 }}>Potassium (K)</label>
                <span style={{ fontSize: "13px", fontWeight: 700, color: "#d97706" }}>{form.K} kg/ha</span>
              </div>
              <input
                type="range"
                min="5"
                max="210"
                value={form.K}
                onChange={(e) => setForm({ ...form, K: Number(e.target.value) })}
                className="slider-range"
              />
            </div>

            {/* Soil pH */}
            <div className="form-group">
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                <label className="form-label" style={{ margin: 0 }}>Soil pH</label>
                <span style={{ fontSize: "13px", fontWeight: 700, color: "#7c3aed" }}>{form.ph.toFixed(1)}</span>
              </div>
              <input
                type="range"
                min="4.0"
                max="9.0"
                step="0.1"
                value={form.ph}
                onChange={(e) => setForm({ ...form, ph: Number(e.target.value) })}
                className="slider-range"
              />
            </div>

            {/* Climate Row */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(90px, 1fr))", gap: "10px", marginTop: "14px", marginBottom: "18px" }}>
              <div className="form-group" style={{ margin: 0 }}>
                <label className="form-label" style={{ fontSize: "11px" }}>Rainfall (mm)</label>
                <input
                  type="number"
                  value={form.rainfall}
                  onChange={(e) => setForm({ ...form, rainfall: Number(e.target.value) })}
                  className="form-input"
                  style={{ padding: "8px 10px", fontSize: "13px" }}
                />
              </div>
              <div className="form-group" style={{ margin: 0 }}>
                <label className="form-label" style={{ fontSize: "11px" }}>Temp (°C)</label>
                <input
                  type="number"
                  value={form.temperature}
                  onChange={(e) => setForm({ ...form, temperature: Number(e.target.value) })}
                  className="form-input"
                  style={{ padding: "8px 10px", fontSize: "13px" }}
                />
              </div>
              <div className="form-group" style={{ margin: 0 }}>
                <label className="form-label" style={{ fontSize: "11px" }}>Humidity (%)</label>
                <input
                  type="number"
                  value={form.humidity}
                  onChange={(e) => setForm({ ...form, humidity: Number(e.target.value) })}
                  className="form-input"
                  style={{ padding: "8px 10px", fontSize: "13px" }}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
              style={{ width: "100%", padding: "12px", fontSize: "14px" }}
            >
              {loading ? "Analyzing Agronomic Suitability..." : "Predict Recommended Crops"}
            </button>
          </form>
        </div>

        {/* Right Column: Prediction Results & Feature Importance */}
        <div>
          {result && (
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              {/* Top Recommended Crop Hero Card */}
              <div style={{
                background: "linear-gradient(135deg, #065f46 0%, #047857 100%)",
                color: "#ffffff",
                borderRadius: "16px",
                padding: "20px 24px",
                boxShadow: "0 8px 16px rgba(4, 120, 87, 0.2)"
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "6px" }}>
                  <span style={{ fontSize: "11px", color: "#a7f3d0", fontWeight: 700, textTransform: "uppercase" }}>
                    Top Recommendation
                  </span>
                  <span style={{ background: "rgba(255,255,255,0.2)", padding: "3px 10px", borderRadius: "9999px", fontSize: "12px", fontWeight: 700 }}>
                    {result.recommendations[0]?.percentage} Match
                  </span>
                </div>
                <h2 style={{ fontSize: "28px", fontWeight: 800, margin: "0 0 6px 0" }}>
                  {result.top_crop}
                </h2>
                <p style={{ fontSize: "13px", color: "#d1fae5", margin: "0 0 14px 0", lineHeight: 1.4 }}>
                  {result.recommendations[0]?.soil_suitability} based on soil NPK profile.
                </p>

                <div style={{ display: "flex", flexWrap: "wrap", gap: "14px", paddingTop: "12px", borderTop: "1px solid rgba(255,255,255,0.2)", fontSize: "12px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                    <Clock size={14} color="#a7f3d0" />
                    <span>Duration: <strong>{result.recommendations[0]?.expected_duration_days}</strong></span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                    <Droplets size={14} color="#a7f3d0" />
                    <span>Water: <strong>{result.recommendations[0]?.water_requirement}</strong></span>
                  </div>
                </div>
              </div>

              {/* Other Top-K Crops */}
              <div className="card">
                <h3 style={{ fontSize: "14px", fontWeight: 800, color: "#0f172a", marginBottom: "12px" }}>
                  Alternative Suitable Crops
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                  {result.recommendations.map((rec, idx) => (
                    <div key={idx} style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      padding: "10px 14px",
                      background: idx === 0 ? "#f0fdf4" : "#f8fafc",
                      border: `1px solid ${idx === 0 ? "#bbf7d0" : "#e2e8f0"}`,
                      borderRadius: "8px"
                    }}>
                      <div>
                        <div style={{ fontSize: "14px", fontWeight: 700, color: "#0f172a" }}>
                          {idx + 1}. {rec.crop}
                        </div>
                        <div style={{ fontSize: "11px", color: "#64748b" }}>
                          {rec.key_advantages.slice(0, 1).join(", ")}
                        </div>
                      </div>
                      <span className={`badge ${idx === 0 ? "badge-green" : "badge-blue"}`} style={{ fontSize: "11px" }}>
                        {rec.percentage} Match
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Feature Importance Recharts Bar Chart */}
              <div className="card">
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
                  <h3 style={{ fontSize: "14px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
                    Agronomic Factor Influence Breakdown
                  </h3>
                  <span style={{ fontSize: "11px", color: "#64748b" }}>Weight %</span>
                </div>
                <div style={{ height: "160px", width: "100%" }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} layout="vertical" margin={{ left: 10, right: 15, top: 0, bottom: 0 }}>
                      <XAxis type="number" domain={[0, 30]} tick={{ fontSize: 10 }} />
                      <YAxis type="category" dataKey="feature" tick={{ fontSize: 10 }} width={75} />
                      <Tooltip formatter={(val) => [`${val}%`, "Weight"]} />
                      <Bar dataKey="importance" fill="#059669" radius={[0, 4, 4, 0]}>
                        {chartData.map((_, index) => (
                          <Cell key={`cell-${index}`} fill={index === 0 ? "#059669" : index === 1 ? "#10b981" : "#34d399"} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* GoI District Crop Production Context (Dataset 8) */}
              {result.district_context && result.district_context.top_historically_produced_crops && (
                <div className="card" style={{ background: "#f0fdf4", border: "1px solid #bbf7d0" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "13px", fontWeight: 700, color: "#166534", marginBottom: "6px" }}>
                    <BarChart3 size={15} /> GoI District Production Statistics ({result.district_context.state}):
                  </div>
                  <div style={{ fontSize: "12px", color: "#15803d", lineHeight: 1.5, marginBottom: "4px" }}>
                    • <strong>Top Historically Cultivated Crops:</strong> {result.district_context.top_historically_produced_crops.join(", ")}
                  </div>
                  <div style={{ fontSize: "11px", color: "#166534", fontStyle: "italic" }}>
                    💡 {result.district_context.historical_note}
                  </div>
                </div>
              )}

              {/* Soil Health Insights */}
              <div style={{ background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: "10px", padding: "12px 14px" }}>
                <h4 style={{ fontSize: "12px", fontWeight: 700, color: "#334155", marginBottom: "6px" }}>
                  Soil Health Diagnostic:
                </h4>
                {Object.entries(result.nutritional_analysis).map(([nut, text], i) => (
                  <div key={i} style={{ fontSize: "11px", color: "#475569", marginBottom: "3px" }}>
                    • <strong>{nut}:</strong> {text}
                  </div>
                ))}
                <div style={{ fontSize: "10px", color: "#94a3b8", marginTop: "6px", borderTop: "1px solid #e2e8f0", paddingTop: "4px" }}>
                  {result.disclaimer}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
