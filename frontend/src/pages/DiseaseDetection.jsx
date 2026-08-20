import React, { useState, useEffect } from "react";
import { useFarmer } from "../context/FarmerContext";
import {
  diagnoseLeafFile,
  diagnoseSampleLeaf,
  getDiseaseSamples,
  getDiseaseClasses
} from "../services/api";
import {
  Bug,
  UploadCloud,
  CheckCircle,
  AlertTriangle,
  ShieldCheck,
  FlaskConical,
  Sprout,
  Image as ImageIcon,
  Sparkles,
  RefreshCw,
  Info,
  Camera,
  BotMessageSquare,
  FileText,
  Terminal,
  ChevronDown,
  ChevronUp,
  ShieldAlert,
  HelpCircle,
  AlertCircle
} from "lucide-react";

export default function DiseaseDetection() {
  const { 
    setShowCameraScanner, 
    askAiAboutDisease, 
    setShowActionPlanModal, 
    refreshActionPlan 
  } = useFarmer();

  const [samples, setSamples] = useState([]);
  const [selectedSample, setSelectedSample] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showDebugPanel, setShowDebugPanel] = useState(false);

  useEffect(() => {
    getDiseaseSamples().then((data) => {
      setSamples(data);
    }).catch(console.error);
  }, []);

  const resetStateForNewInput = () => {
    setResult(null);
    setError(null);
    setLoading(true);
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadedFile(file);
    setSelectedSample(null);
    setImagePreview(URL.createObjectURL(file));
    resetStateForNewInput();

    try {
      const res = await diagnoseLeafFile(file);
      setResult(res);
    } catch (err) {
      setError(err.message || "Failed to process image");
    } finally {
      setLoading(false);
    }
  };

  const handleDiagnoseSample = async (filename) => {
    setSelectedSample(filename);
    setUploadedFile(null);
    setImagePreview(`http://127.0.0.1:8000/static/samples/${filename}`);
    resetStateForNewInput();

    try {
      const res = await diagnoseSampleLeaf(filename);
      setResult(res);
    } catch (err) {
      setError(err.message || "Failed to diagnose sample");
    } finally {
      setLoading(false);
    }
  };

  const handleAskAi = () => {
    if (result) {
      askAiAboutDisease(result, imagePreview);
    }
  };

  return (
    <div className="page-wrapper">
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "20px", flexWrap: "wrap", gap: "12px" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
            <span className="badge badge-purple">AI Disease Detection</span>
            <span style={{ fontSize: "12px", color: "#64748b", fontWeight: 600 }}>Computer Vision Leaf Diagnosis</span>
          </div>
          <h1 style={{ fontSize: "24px", fontWeight: 800, color: "#0f172a", letterSpacing: "-0.02em", margin: 0 }}>
            Plant Leaf Disease Detection & Cure
          </h1>
          <p style={{ fontSize: "13px", color: "#64748b", marginTop: "4px" }}>
            Use phone camera or upload a leaf photograph for instant AI pathogen diagnosis, confidence verification, and organic/chemical remedies.
          </p>
        </div>

        {/* Prominent Live Camera Action Button */}
        <button
          onClick={() => setShowCameraScanner(true)}
          className="btn btn-primary"
          style={{ padding: "10px 18px", fontSize: "14px", background: "linear-gradient(135deg, #059669 0%, #047857 100%)", boxShadow: "0 4px 12px rgba(5, 150, 105, 0.25)" }}
        >
          <Camera size={18} />
          <span><strong>📷 Open Camera Scanner</strong></span>
        </button>
      </div>

      <div className="grid-2">
        {/* Left Column: Image Upload & Sample Gallery */}
        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          {/* Upload & Camera Dropzone */}
          <div className="card" style={{ textAlign: "center", borderStyle: "dashed", borderWidth: "2px", borderColor: "#059669", padding: "20px 14px" }}>
            <input
              type="file"
              id="leaf-upload"
              accept="image/*"
              capture="environment"
              onChange={handleFileUpload}
              style={{ display: "none" }}
            />
            
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "10px" }}>
              <div style={{ width: "50px", height: "50px", borderRadius: "50%", background: "#ecfdf5", color: "#059669", display: "flex", alignItems: "center", justifyContent: "center" }}>
                <UploadCloud size={26} />
              </div>
              <div>
                <div style={{ fontSize: "15px", fontWeight: 700, color: "#0f172a" }}>
                  Take Photo or Upload Leaf Image
                </div>
                <div style={{ fontSize: "12px", color: "#64748b", marginTop: "2px" }}>
                  JPG, JPEG, PNG from Camera or Gallery
                </div>
              </div>

              <div style={{ display: "flex", gap: "10px", marginTop: "6px", flexWrap: "wrap", justifyContent: "center" }}>
                <button
                  type="button"
                  onClick={() => setShowCameraScanner(true)}
                  className="btn btn-primary"
                  style={{ padding: "8px 16px", fontSize: "13px" }}
                >
                  <Camera size={15} /> Open Camera
                </button>

                <label
                  htmlFor="leaf-upload"
                  className="btn btn-secondary"
                  style={{ padding: "8px 16px", fontSize: "13px", cursor: "pointer" }}
                >
                  Browse Gallery
                </label>
              </div>
            </div>
          </div>

          {/* Preset Sample Leaf Test Gallery */}
          <div className="card">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
              <div>
                <h3 style={{ fontSize: "14px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
                  Instant Test Gallery (Ground-Truth Samples)
                </h3>
                <div style={{ fontSize: "11px", color: "#64748b", marginTop: "2px" }}>
                  Tap any sample leaf to run inference through the AI vision pipeline
                </div>
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "8px" }}>
              {samples.map((s, idx) => (
                <div
                  key={idx}
                  onClick={() => handleDiagnoseSample(s.filename)}
                  style={{
                    border: `2px solid ${selectedSample === s.filename ? "#059669" : "#e2e8f0"}`,
                    borderRadius: "8px",
                    overflow: "hidden",
                    cursor: "pointer",
                    background: selectedSample === s.filename ? "#ecfdf5" : "#f8fafc",
                    textAlign: "center",
                    padding: "4px",
                    transition: "all 0.15s ease"
                  }}
                >
                  <img
                    src={`http://127.0.0.1:8000${s.url}`}
                    alt={s.label}
                    style={{ width: "100%", height: "55px", objectFit: "cover", borderRadius: "6px", marginBottom: "2px" }}
                  />
                  <div style={{ fontSize: "9px", fontWeight: 600, color: "#334155", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                    {s.label.replace("Tomato ", "").replace("Potato ", "").replace("Corn ", "").replace("Apple ", "").replace("Grape ", "")}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Active Image Input Preview */}
          {imagePreview && (
            <div className="card" style={{ display: "flex", alignItems: "center", gap: "14px", padding: "14px" }}>
              <img
                src={imagePreview}
                alt="Leaf Preview"
                style={{ width: "80px", height: "80px", objectFit: "cover", borderRadius: "10px", border: "1px solid #e2e8f0", flexShrink: 0 }}
              />
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                  <span className={`badge ${selectedSample ? "badge-blue" : "badge-green"}`} style={{ fontSize: "10px" }}>
                    {selectedSample ? "Demo Test Sample" : "User Upload"}
                  </span>
                  {result && (
                    <span style={{ fontSize: "10px", color: "#64748b", fontFamily: "monospace" }}>
                      ID: {result.request_id || "DX-2026"}
                    </span>
                  )}
                </div>
                <div style={{ fontSize: "14px", fontWeight: 700, color: "#0f172a", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", marginTop: "2px" }}>
                  {uploadedFile ? uploadedFile.name : selectedSample}
                </div>
                <div style={{ fontSize: "12px", color: loading ? "#d97706" : "#059669", fontWeight: 600, marginTop: "2px" }}>
                  Status: {loading ? "Analyzing leaf features..." : "Diagnosis Completed"}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Diagnosis Results & Remedies */}
        <div>
          {!loading && !result && !error && (
            <div className="card" style={{ textAlign: "center", padding: "60px 20px" }}>
              <div style={{ width: "60px", height: "60px", borderRadius: "50%", background: "#f0fdf4", color: "#16a34a", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 16px" }}>
                <Bug size={32} />
              </div>
              <h3 style={{ fontSize: "16px", fontWeight: 700, color: "#0f172a", marginBottom: "6px" }}>
                Ready to Analyze Leaf Health
              </h3>
              <p style={{ fontSize: "13px", color: "#64748b", maxWidth: "360px", margin: "0 auto 18px", lineHeight: 1.5 }}>
                Select a sample leaf from the gallery or upload your own leaf photo to run real-time AI vision pathogen classification.
              </p>
              <button
                onClick={() => setShowCameraScanner(true)}
                className="btn btn-primary"
                style={{ padding: "10px 20px" }}
              >
                <Camera size={16} /> Open Camera Scanner
              </button>
            </div>
          )}

          {loading && (
            <div className="card" style={{ textAlign: "center", padding: "60px 20px" }}>
              <div style={{ display: "inline-block", animation: "spin 1s infinite linear" }}>
                <RefreshCw size={32} color="#059669" />
              </div>
              <div style={{ marginTop: "16px", fontSize: "16px", fontWeight: 700, color: "#0f172a" }}>
                Running Computer Vision Inference...
              </div>
              <div style={{ fontSize: "12px", color: "#64748b", marginTop: "4px" }}>
                Extracting multi-scale spatial color moments & matching against 27 plant disease classes
              </div>
            </div>
          )}

          {error && (
            <div className="card" style={{ background: "#fee2e2", borderColor: "#fecaca", color: "#991b1b" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px", fontWeight: 700 }}>
                <AlertTriangle size={18} /> Error Processing Image
              </div>
              <div style={{ fontSize: "13px", marginTop: "4px" }}>{error}</div>
            </div>
          )}

          {!loading && result && (
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              
              {/* ⚠️ LOW CONFIDENCE / UNCERTAIN WARNING BANNER */}
              {result.is_low_confidence ? (
                <div style={{
                  background: "linear-gradient(135deg, #7c2d12 0%, #9a3412 100%)",
                  color: "#ffffff",
                  borderRadius: "16px",
                  padding: "20px 24px",
                  boxShadow: "0 8px 16px rgba(154, 52, 18, 0.2)"
                }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
                    <span style={{ background: "rgba(255,255,255,0.2)", padding: "3px 10px", borderRadius: "9999px", fontSize: "11px", fontWeight: 700, textTransform: "uppercase" }}>
                      ⚠️ Low Model Confidence ({result.confidence_percentage})
                    </span>
                    <span style={{ fontSize: "11px", color: "rgba(255,255,255,0.8)", fontFamily: "monospace" }}>
                      ID: {result.request_id}
                    </span>
                  </div>

                  <h2 style={{ fontSize: "20px", fontWeight: 800, margin: "0 0 8px 0" }}>
                    Uncertain Plant Condition
                  </h2>

                  <p style={{ fontSize: "13px", color: "rgba(255,255,255,0.9)", lineHeight: 1.5, margin: "0 0 14px 0" }}>
                    The AI vision model could not confidently identify this leaf condition (Highest match: {result.top_predictions?.[0]?.crop} {result.top_predictions?.[0]?.condition} at {result.confidence_percentage}).
                  </p>

                  <div style={{ background: "rgba(0,0,0,0.2)", borderRadius: "10px", padding: "12px", fontSize: "12px", lineHeight: 1.5 }}>
                    <strong>Possible Reasons:</strong>
                    <ul style={{ margin: "4px 0 0 16px", padding: 0 }}>
                      <li>Image lighting is too dim or overexposed</li>
                      <li>Affected leaf portion is out of focus or far away</li>
                      <li>Crop species or disease condition is not supported in the 27 PlantVillage classes</li>
                    </ul>
                  </div>

                  <div style={{ display: "flex", gap: "10px", marginTop: "16px", flexWrap: "wrap" }}>
                    <button
                      onClick={() => setShowCameraScanner(true)}
                      className="btn"
                      style={{ background: "#ffffff", color: "#9a3412", padding: "9px 16px", fontSize: "13px", fontWeight: 700 }}
                    >
                      <Camera size={16} /> Retake Photo
                    </button>
                    <label
                      htmlFor="leaf-upload"
                      className="btn"
                      style={{ background: "rgba(255,255,255,0.2)", color: "#ffffff", padding: "9px 16px", fontSize: "13px", fontWeight: 700, cursor: "pointer" }}
                    >
                      Choose Another Image
                    </label>
                  </div>
                </div>
              ) : (
                /* HIGH / MODERATE CONFIDENCE DIAGNOSIS HERO CARD */
                <div style={{
                  background: result.status === "Healthy" 
                    ? "linear-gradient(135deg, #065f46 0%, #047857 100%)" 
                    : "linear-gradient(135deg, #881337 0%, #be123c 100%)",
                  color: "#ffffff",
                  borderRadius: "16px",
                  padding: "20px 24px",
                  boxShadow: "0 8px 16px rgba(0,0,0,0.12)"
                }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
                    <span style={{ fontSize: "12px", color: "rgba(255,255,255,0.85)", fontWeight: 700, textTransform: "uppercase" }}>
                      Detected Crop: {result.detected_crop}
                    </span>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <span style={{ background: "rgba(255,255,255,0.2)", padding: "3px 10px", borderRadius: "9999px", fontSize: "12px", fontWeight: 700 }}>
                        {result.confidence_percentage} Match ({result.confidence_tier})
                      </span>
                    </div>
                  </div>

                  <h2 style={{ fontSize: "24px", fontWeight: 800, margin: "0 0 6px 0" }}>
                    {result.condition}
                  </h2>

                  <div style={{ display: "flex", alignItems: "center", gap: "10px", marginTop: "6px", fontSize: "12px", flexWrap: "wrap" }}>
                    <span className={`badge ${result.status === "Healthy" ? "badge-green" : "badge-red"}`}>
                      {result.status}
                    </span>
                    <span style={{ color: "rgba(255,255,255,0.9)" }}>
                      Severity: <strong>{result.severity}</strong> • Pathogen: {result.pathogen}
                    </span>
                  </div>

                  {result.confidence_tier === "Moderate Confidence" && (
                    <div style={{ marginTop: "12px", background: "rgba(0,0,0,0.25)", padding: "8px 12px", borderRadius: "8px", fontSize: "11px", display: "flex", alignItems: "center", gap: "6px" }}>
                      <AlertCircle size={14} color="#fde047" />
                      <span>Moderate confidence prediction. Verify leaf symptoms with local Krishi Vigyan Kendra (KVK) officer before applying chemical sprays.</span>
                    </div>
                  )}
                </div>
              )}

              {/* Action Buttons: Ask AI & Scan Another Leaf */}
              <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                <button
                  onClick={handleAskAi}
                  className="btn btn-primary"
                  style={{ flex: 1.5, minWidth: "180px", padding: "12px 16px", fontSize: "13px", justifyContent: "center" }}
                >
                  <BotMessageSquare size={16} />
                  <span><strong>💬 Ask AI About This Disease</strong></span>
                </button>

                <button
                  onClick={() => setShowCameraScanner(true)}
                  className="btn btn-secondary"
                  style={{ flex: 1, minWidth: "140px", padding: "12px 14px", fontSize: "13px", justifyContent: "center" }}
                >
                  <Camera size={16} />
                  <span>Scan Another Leaf</span>
                </button>
              </div>

              {/* Symptoms & Immediate Action */}
              <div className="card">
                <h3 style={{ fontSize: "14px", fontWeight: 800, color: "#0f172a", marginBottom: "8px" }}>
                  Symptoms & Immediate Action
                </h3>
                <div style={{ fontSize: "13px", color: "#334155", marginBottom: "10px", lineHeight: 1.5 }}>
                  <strong>Symptoms:</strong> {result.symptoms}
                </div>
                <div style={{ background: result.is_low_confidence ? "#fef3c7" : "#fef2f2", border: `1px solid ${result.is_low_confidence ? "#fde68a" : "#fecaca"}`, borderRadius: "8px", padding: "10px 12px", fontSize: "13px", color: result.is_low_confidence ? "#92400e" : "#991b1b" }}>
                  <strong>Immediate Action:</strong> {result.immediate_actions}
                </div>
              </div>

              {/* Treatment Protocols (Organic vs Chemical) */}
              <div className="grid-2">
                <div className="card card-gradient">
                  <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "#065f46", fontWeight: 700, fontSize: "13px", marginBottom: "6px" }}>
                    <Sprout size={15} /> Organic / Bio Treatment
                  </div>
                  <div style={{ fontSize: "12px", color: "#1e293b", lineHeight: 1.5 }}>
                    {result.organic_treatment}
                  </div>
                </div>

                <div className="card" style={{ background: result.is_low_confidence ? "#f8fafc" : "#fff7ed", border: `1px solid ${result.is_low_confidence ? "#e2e8f0" : "#fed7aa"}` }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "6px", color: result.is_low_confidence ? "#64748b" : "#9a3412", fontWeight: 700, fontSize: "13px", marginBottom: "6px" }}>
                    <FlaskConical size={15} /> Chemical Spray / Dosage
                  </div>
                  <div style={{ fontSize: "12px", color: result.is_low_confidence ? "#64748b" : "#1e293b", lineHeight: 1.5, fontStyle: result.is_low_confidence ? "italic" : "normal" }}>
                    {result.chemical_treatment}
                  </div>
                </div>
              </div>

              {/* Prevention & Disclaimer */}
              <div style={{ background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: "12px", padding: "14px" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "12px", fontWeight: 700, color: "#334155", marginBottom: "4px" }}>
                  <ShieldCheck size={15} color="#059669" /> Preventative Cultural Practices
                </div>
                <div style={{ fontSize: "12px", color: "#475569", lineHeight: 1.5, marginBottom: "8px" }}>
                  {result.prevention_measures}
                </div>
                <div style={{ fontSize: "10px", color: "#94a3b8", borderTop: "1px solid #e2e8f0", paddingTop: "6px" }}>
                  {result.disclaimer}
                </div>
              </div>

              {/* 🐞 DEVELOPER DIAGNOSTIC DEBUG DRAWER */}
              <div className="card" style={{ background: "#0f172a", color: "#e2e8f0", padding: "14px 18px", borderRadius: "12px" }}>
                <div 
                  onClick={() => setShowDebugPanel(!showDebugPanel)}
                  style={{ display: "flex", justifyContent: "space-between", alignItems: "center", cursor: "pointer" }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "13px", fontWeight: 700, color: "#38bdf8" }}>
                    <Terminal size={16} /> Developer Diagnostic View (Request ID: {result.request_id || "DX-2026"})
                  </div>
                  <div style={{ color: "#94a3b8", display: "flex", alignItems: "center", gap: "4px", fontSize: "12px" }}>
                    {showDebugPanel ? "Hide Details" : "Show Model Details"}
                    {showDebugPanel ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                  </div>
                </div>

                {showDebugPanel && result.debug_info && (
                  <div style={{ marginTop: "14px", borderTop: "1px solid #334155", paddingTop: "12px", fontSize: "12px", fontFamily: "monospace" }}>
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: "8px", marginBottom: "12px" }}>
                      <div><span style={{ color: "#94a3b8" }}>Filename:</span> {result.debug_info.filename}</div>
                      <div><span style={{ color: "#94a3b8" }}>Image Size:</span> {result.debug_info.image_size_bytes} bytes</div>
                      <div><span style={{ color: "#94a3b8" }}>Features Dim:</span> {result.debug_info.extracted_features_dim} (Multi-scale color moments)</div>
                      <div><span style={{ color: "#94a3b8" }}>Total Classes:</span> {result.debug_info.total_model_classes} PlantVillage categories</div>
                      <div><span style={{ color: "#94a3b8" }}>Confidence Tier:</span> {result.debug_info.confidence_tier}</div>
                      <div><span style={{ color: "#94a3b8" }}>Out-of-Distribution:</span> {result.debug_info.is_out_of_distribution ? "YES (Low Confidence)" : "NO"}</div>
                    </div>

                    <div style={{ fontWeight: 700, color: "#f1f5f9", marginBottom: "6px" }}>Top 3 Model Probability Distribution:</div>
                    <div style={{ background: "#1e293b", borderRadius: "8px", padding: "8px", overflowX: "auto" }}>
                      <table style={{ width: "100%", textWrap: "nowrap", borderCollapse: "collapse" }}>
                        <thead>
                          <tr style={{ borderBottom: "1px solid #475569", color: "#94a3b8", textAlign: "left" }}>
                            <th style={{ padding: "4px" }}>Rank</th>
                            <th style={{ padding: "4px" }}>Class ID</th>
                            <th style={{ padding: "4px" }}>Crop & Condition</th>
                            <th style={{ padding: "4px" }}>Probability</th>
                          </tr>
                        </thead>
                        <tbody>
                          {result.top_predictions?.map((pred, i) => (
                            <tr key={i} style={{ borderBottom: "1px solid #334155", color: i === 0 ? "#4ade80" : "#cbd5e1" }}>
                              <td style={{ padding: "4px" }}>#{i + 1}</td>
                              <td style={{ padding: "4px" }}>{pred.class_id}</td>
                              <td style={{ padding: "4px" }}>{pred.crop} - {pred.condition}</td>
                              <td style={{ padding: "4px", fontWeight: 700 }}>{pred.confidence_percentage}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>

            </div>
          )}
        </div>
      </div>
    </div>
  );
}
