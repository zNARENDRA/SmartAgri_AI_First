import React, { useState, useEffect } from "react";
import { getModelsSummary, getDataRegistry } from "../services/api";
import {
  Database,
  Award,
  Layers,
  ShieldCheck,
  ExternalLink,
  Table,
  BarChart3,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Info
} from "lucide-react";

export default function ModelEvaluationInfo() {
  const [summary, setSummary] = useState(null);
  const [registry, setRegistry] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getModelsSummary(), getDataRegistry()])
      .then(([sumData, regData]) => {
        setSummary(sumData);
        setRegistry(regData);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="page-wrapper" style={{ textAlign: "center", padding: "60px 20px" }}>
        <div style={{ display: "inline-block", animation: "spin 1s infinite linear" }}>
          <RefreshCw size={32} color="#059669" />
        </div>
        <div style={{ marginTop: "12px", color: "#64748b" }}>Loading technology documentation & data sources registry...</div>
      </div>
    );
  }

  const cropAlgos = summary?.crop_recommendation_metrics?.algorithm_comparison || {};
  const yieldAlgos = summary?.crop_yield_metrics?.algorithm_comparison || {};
  const sourcesList = registry?.sources || [];

  return (
    <div className="page-wrapper">
      {/* Header */}
      <div style={{ marginBottom: "20px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
          <span className="badge badge-green">Technical Transparency</span>
          <span style={{ fontSize: "12px", color: "#64748b", fontWeight: 600 }}>11 Integrated Datasets & AI Registry</span>
        </div>
        <h1 style={{ fontSize: "24px", fontWeight: 800, color: "#0f172a", letterSpacing: "-0.02em", margin: 0 }}>
          Agricultural Data & AI Model Architecture Registry
        </h1>
        <p style={{ fontSize: "13px", color: "#64748b", marginTop: "2px" }}>
          Complete provenance, provider attributions, URLs, license information, and machine learning benchmarks across all 11 agricultural datasets.
        </p>
      </div>

      {/* Datasets Provenance Section */}
      <div className="card" style={{ marginBottom: "24px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px", flexWrap: "wrap", gap: "8px" }}>
          <h2 style={{ fontSize: "16px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
            📚 11 Integrated Agricultural Data Sources & AI Registry
          </h2>
          <span className="badge badge-blue">
            Total Records: {registry?.total_records?.toLocaleString() || "100,000+"}
          </span>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
          {sourcesList.map((d, idx) => (
            <div
              key={idx}
              style={{
                border: "1px solid #e2e8f0",
                borderRadius: "10px",
                padding: "16px",
                background: "#f8fafc"
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "6px", flexWrap: "wrap", gap: "8px" }}>
                <div>
                  <span className="badge badge-green" style={{ fontSize: "10px", marginBottom: "4px" }}>{d.category}</span>
                  <h3 style={{ fontSize: "15px", fontWeight: 800, color: "#0f172a", margin: "2px 0" }}>
                    {d.id.toUpperCase()} — {d.name}
                  </h3>
                </div>

                <a
                  href={d.url}
                  target="_blank"
                  rel="noreferrer"
                  className="btn btn-secondary"
                  style={{ padding: "5px 10px", fontSize: "11px", minHeight: "32px" }}
                >
                  <span>Verify Data Source</span>
                  <ExternalLink size={11} />
                </a>
              </div>

              <p style={{ fontSize: "12px", color: "#334155", margin: "0 0 8px 0", lineHeight: 1.4 }}>
                <strong>Attribution & Description:</strong> {d.attribution}
              </p>

              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))", gap: "8px", fontSize: "11px", color: "#475569", background: "#ffffff", padding: "10px 14px", borderRadius: "8px", border: "1px solid #e2e8f0" }}>
                <div>
                  <strong>Data Provider:</strong> {d.provider}
                </div>
                <div>
                  <strong>Records / Entries:</strong> {d.records?.toLocaleString()}
                </div>
                <div>
                  <strong>Platform Module Used:</strong> <span style={{ color: "#059669", fontWeight: 700 }}>{d.module_used}</span>
                </div>
              </div>

              <div style={{ fontSize: "11px", color: "#64748b", marginTop: "8px" }}>
                <strong>License:</strong> {d.license}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Model Benchmark Comparison Tables */}
      <div className="grid-2" style={{ marginBottom: "24px" }}>
        {/* Table 1: Crop Recommendation Classifiers */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
            <h3 style={{ fontSize: "15px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
              🌱 Crop Recommendation Benchmark
            </h3>
            <span className="badge badge-green" style={{ fontSize: "10px" }}>5-Fold Cross Validation</span>
          </div>

          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", minWidth: "320px", borderCollapse: "collapse", fontSize: "11px", textAlign: "left" }}>
              <thead>
                <tr style={{ background: "#f8fafc", borderBottom: "2px solid #e2e8f0" }}>
                  <th style={{ padding: "8px" }}>Algorithm</th>
                  <th style={{ padding: "8px" }}>Test Accuracy</th>
                  <th style={{ padding: "8px" }}>F1 Score</th>
                  <th style={{ padding: "8px" }}>CV Mean</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(cropAlgos).map(([name, m]) => (
                  <tr key={name} style={{ borderBottom: "1px solid #f1f5f9", background: name === "Random Forest" ? "#f0fdf4" : "#ffffff" }}>
                    <td style={{ padding: "8px", fontWeight: 700, color: name === "Random Forest" ? "#059669" : "#1e293b" }}>
                      {name} {name === "Random Forest" && "🏆 (Deployed)"}
                    </td>
                    <td style={{ padding: "8px", fontWeight: 700 }}>{(m.test_accuracy * 100).toFixed(1)}%</td>
                    <td style={{ padding: "8px" }}>{(m.f1_weighted * 100).toFixed(1)}%</td>
                    <td style={{ padding: "8px" }}>{(m.cv_mean_accuracy * 100).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Table 2: Crop Yield Regressors */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
            <h3 style={{ fontSize: "15px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
              📈 Crop Yield Regressor Benchmark
            </h3>
            <span className="badge badge-amber" style={{ fontSize: "10px" }}>R² / MAE</span>
          </div>

          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", minWidth: "320px", borderCollapse: "collapse", fontSize: "11px", textAlign: "left" }}>
              <thead>
                <tr style={{ background: "#f8fafc", borderBottom: "2px solid #e2e8f0" }}>
                  <th style={{ padding: "8px" }}>Algorithm</th>
                  <th style={{ padding: "8px" }}>R² Score</th>
                  <th style={{ padding: "8px" }}>MAE (T/Ha)</th>
                  <th style={{ padding: "8px" }}>RMSE</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(yieldAlgos).map(([name, m]) => (
                  <tr key={name} style={{ borderBottom: "1px solid #f1f5f9", background: name.includes("Gradient") ? "#fffbeb" : "#ffffff" }}>
                    <td style={{ padding: "8px", fontWeight: 700, color: name.includes("Gradient") ? "#d97706" : "#1e293b" }}>
                      {name} {name.includes("Gradient") && "🏆 (Deployed)"}
                    </td>
                    <td style={{ padding: "8px", fontWeight: 700 }}>{m.R2_Score?.toFixed(4)}</td>
                    <td style={{ padding: "8px" }}>{m.MAE?.toFixed(2)}</td>
                    <td style={{ padding: "8px" }}>{m.RMSE?.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* AI Safety and Ethical Advisory Safeguards */}
      <div className="card" style={{ background: "#f8fafc", borderLeft: "4px solid #059669" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
          <ShieldCheck size={18} color="#059669" />
          <h3 style={{ fontSize: "15px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
            Safety, Reliability & Ethical Decision Support
          </h3>
        </div>
        <p style={{ fontSize: "12px", color: "#475569", lineHeight: 1.5, margin: 0 }}>
          1. <strong>Uncertainty Communication:</strong> Every recommendation reports confidence levels and probabilistic ranges. We avoid claiming deterministic guarantees.<br />
          2. <strong>Grounding in Real Agricultural Datasets:</strong> All backend endpoints query real trained models and cleaned datasets (Agmarknet, PlantVillage, ICAR, DA&FW).<br />
          3. <strong>Human Expert Verification:</strong> Farmers are advised to confirm critical high-expenditure chemical spray choices with local Krishi Vigyan Kendra (KVK) extension officers.
        </p>
      </div>
    </div>
  );
}
