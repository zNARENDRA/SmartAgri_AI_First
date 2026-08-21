import React, { useState, useEffect, useRef } from "react";
import { useFarmer } from "../context/FarmerContext";
import {
  predictCrop,
  predictYield,
  getMarketTrends,
  getWhereToSell,
  matchSchemesProfile
} from "../services/api";
import {
  Sprout,
  TrendingUp,
  CloudSun,
  Store,
  Landmark,
  AlertTriangle,
  ArrowRight,
  Sparkles,
  Droplets,
  CheckCircle2,
  Calendar,
  Activity,
  FileText,
  Camera,
  Image as ImageIcon,
  Plus
} from "lucide-react";

export default function Dashboard() {
  const { 
    profile, 
    weather, 
    setActiveTab, 
    refreshActionPlan, 
    setShowActionPlanModal,
    setShowCameraScanner,
    fieldPhotos,
    addFieldPhoto
  } = useFarmer();

  const [topCropRec, setTopCropRec] = useState(null);
  const [yieldData, setYieldData] = useState(null);
  const [marketData, setMarketData] = useState(null);
  const [bestMandi, setBestMandi] = useState(null);
  const [topSchemes, setTopSchemes] = useState([]);
  const [loading, setLoading] = useState(true);

  const fieldPhotoInputRef = useRef(null);

  useEffect(() => {
    async function loadDashboardData() {
      setLoading(true);
      try {
        // 1. Crop Recommendation for profile
        const cRes = await predictCrop({
          N: profile.nitrogen,
          P: profile.phosphorus,
          K: profile.potassium,
          temperature: 26.5,
          humidity: 65.0,
          ph: profile.soil_ph,
          rainfall: 105.0,
          top_k: 1
        });
        setTopCropRec(cRes.recommendations[0]);

        // 2. Yield Prediction for current crop
        const yCrop = profile.current_crop || cRes.top_crop || "Wheat";
        const yRes = await predictYield({
          crop: yCrop,
          state: profile.state,
          season: profile.farming_season || "Kharif",
          area: profile.land_size_acres / 2.471, // Convert acres to hectares
          annual_rainfall: 1050.0,
          fertilizer: 110.0,
          pesticide: 1.5
        });
        setYieldData(yRes);

        // 3. Market Trends for current crop
        const mRes = await getMarketTrends(yCrop, profile.state, profile.district);
        setMarketData(mRes);

        const wSell = await getWhereToSell(yCrop, profile.state);
        if (wSell.best_mandis && wSell.best_mandis.length > 0) {
          setBestMandi(wSell.best_mandis[0]);
        }

        // 4. Matched Schemes
        const sRes = await matchSchemesProfile(profile);
        setTopSchemes(sRes.slice(0, 3));
      } catch (err) {
        console.error("Dashboard data load error:", err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboardData();
  }, [profile]);

  const handleOpenActionPlan = async () => {
    await refreshActionPlan();
    setShowActionPlanModal(true);
  };

  const handleFieldPhotoUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      addFieldPhoto(event.target.result);
    };
    reader.readAsDataURL(file);
  };

  return (
    <div className="page-wrapper">
      {/* 1. Top Farmer Welcome Banner */}
      <div className="dashboard-welcome-banner">
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "12px", color: "#a7f3d0", fontWeight: 600, marginBottom: "4px" }}>
            <Sparkles size={14} /> SmartAgri — AI Farm Assistant
          </div>
          <h1 style={{ fontSize: "24px", fontWeight: 800, letterSpacing: "-0.02em", margin: 0 }}>
            Namaste, {profile.name}!
          </h1>
          <div style={{ fontSize: "13px", color: "#d1fae5", marginTop: "4px" }}>
            {profile.land_size_acres} Acres • {profile.district}, {profile.state} ({profile.farming_season})
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
          {weather && (
            <div style={{ background: "rgba(255,255,255,0.18)", padding: "8px 14px", borderRadius: "10px", backdropFilter: "blur(6px)" }}>
              <div style={{ fontSize: "11px", color: "#d1fae5" }}>Current Weather</div>
              <div style={{ fontSize: "16px", fontWeight: 800 }}>
                {weather.current.temperature.toFixed(1)}°C {weather.current.condition_text.split(" ")[0]}
              </div>
            </div>
          )}
          <button 
            onClick={handleOpenActionPlan}
            className="btn btn-amber"
            style={{ padding: "8px 14px", fontSize: "13px" }}
          >
            <FileText size={15} /> Action Plan
          </button>
        </div>
      </div>

      {/* 2. Mobile-First Primary Actions: Plant Scanner & Field Photo */}
      <div className="dashboard-scanner-cta-card">
        <div style={{ display: "flex", alignItems: "center", gap: "14px", flex: 1 }}>
          <div className="scanner-cta-icon-box">
            <Camera size={26} color="#ffffff" />
          </div>
          <div>
            <div style={{ fontSize: "16px", fontWeight: 800, color: "#065f46" }}>
              Plant Disease Scanner
            </div>
            <div style={{ fontSize: "12px", color: "#047857", marginTop: "2px" }}>
              Scan or capture leaf photo for instant AI diagnosis & cure
            </div>
          </div>
        </div>

        <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", width: "100%", justifyContent: "flex-end" }}>
          {/* Hidden Field Photo Input */}
          <input
            type="file"
            ref={fieldPhotoInputRef}
            accept="image/*"
            capture="environment"
            onChange={handleFieldPhotoUpload}
            style={{ display: "none" }}
          />

          <button
            onClick={() => fieldPhotoInputRef.current?.click()}
            className="btn btn-secondary"
            style={{ fontSize: "13px", padding: "10px 14px", flex: 1, minWidth: "130px", justifyContent: "center" }}
          >
            <ImageIcon size={16} /> Field Photo
          </button>

          <button
            onClick={() => setShowCameraScanner(true)}
            className="btn btn-primary"
            style={{ fontSize: "13px", padding: "10px 18px", flex: 1.5, minWidth: "160px", justifyContent: "center", background: "linear-gradient(135deg, #059669 0%, #047857 100%)" }}
          >
            <Camera size={16} /> <strong>📷 Scan Plant</strong>
          </button>
        </div>
      </div>

      {/* 3. Agro-Meteorological Critical Alert Bar */}
      {weather && weather.advisory && (
        <div style={{
          background: weather.advisory.irrigation_advice.status.includes("SKIP") ? "#fef3c7" : "#ecfdf5",
          border: `1px solid ${weather.advisory.irrigation_advice.status.includes("SKIP") ? "#fde68a" : "#a7f3d0"}`,
          borderRadius: "12px",
          padding: "12px 16px",
          marginBottom: "20px",
          display: "flex",
          alignItems: "center",
          gap: "12px"
        }}>
          <AlertTriangle size={18} color={weather.advisory.irrigation_advice.status.includes("SKIP") ? "#b45309" : "#059669"} style={{ flexShrink: 0 }} />
          <div style={{ flex: 1, fontSize: "12px", color: "#1e293b", lineHeight: 1.4 }}>
            <strong>Advisory:</strong> {weather.advisory.irrigation_advice.action} (Spraying: <strong>{weather.advisory.spraying_window.status}</strong>)
          </div>
          <button 
            onClick={() => setActiveTab("weather")}
            style={{ background: "transparent", border: "none", color: "#059669", fontWeight: 700, fontSize: "12px", cursor: "pointer", display: "flex", alignItems: "center", gap: "2px", flexShrink: 0 }}
          >
            View <ArrowRight size={13} />
          </button>
        </div>
      )}

      {/* 4. Dashboard KPI Grid (4 Stackable Cards) */}
      <div className="grid-4" style={{ marginBottom: "24px" }}>
        {/* Card 1: Soil & Recommended Crop */}
        <div className="card card-gradient" onClick={() => setActiveTab("crop-advisor")} style={{ cursor: "pointer" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
            <span style={{ fontSize: "11px", fontWeight: 700, color: "#065f46", textTransform: "uppercase" }}>Recommended Crop</span>
            <div style={{ background: "#d1fae5", padding: "5px", borderRadius: "6px", color: "#059669" }}>
              <Sprout size={16} />
            </div>
          </div>
          <div style={{ fontSize: "20px", fontWeight: 800, color: "#065f46", marginBottom: "2px" }}>
            {topCropRec ? topCropRec.crop : "Loading..."}
          </div>
          <div style={{ fontSize: "12px", color: "#047857", fontWeight: 600, marginBottom: "8px" }}>
            {topCropRec ? `${topCropRec.percentage} Soil Match` : "Recommended"}
          </div>
          <div style={{ fontSize: "11px", color: "#059669", fontWeight: 700, display: "flex", alignItems: "center", gap: "4px" }}>
            Explore Advisory <ArrowRight size={12} />
          </div>
        </div>

        {/* Card 2: Expected Yield */}
        <div className="card card-amber-gradient" onClick={() => setActiveTab("yield-predictor")} style={{ cursor: "pointer" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
            <span style={{ fontSize: "11px", fontWeight: 700, color: "#92400e", textTransform: "uppercase" }}>Expected Yield</span>
            <div style={{ background: "#fef3c7", padding: "5px", borderRadius: "6px", color: "#d97706" }}>
              <TrendingUp size={16} />
            </div>
          </div>
          <div style={{ fontSize: "20px", fontWeight: 800, color: "#92400e", marginBottom: "2px" }}>
            {yieldData ? `${yieldData.predicted_yield_quintals_per_acre} Qtl/Ac` : "Estimating..."}
          </div>
          <div style={{ fontSize: "12px", color: "#b45309", fontWeight: 600, marginBottom: "8px" }}>
            {yieldData ? `${yieldData.total_expected_production_tons} Tons Total` : "Acreage Projection"}
          </div>
          <div style={{ fontSize: "11px", color: "#d97706", fontWeight: 700, display: "flex", alignItems: "center", gap: "4px" }}>
            Yield Analysis <ArrowRight size={12} />
          </div>
        </div>

        {/* Card 3: Mandi Price Snapshot */}
        <div className="card card-blue-gradient" onClick={() => setActiveTab("market")} style={{ cursor: "pointer" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
            <span style={{ fontSize: "11px", fontWeight: 700, color: "#0369a1", textTransform: "uppercase" }}>Mandi Price</span>
            <div style={{ background: "#e0f2fe", padding: "5px", borderRadius: "6px", color: "#0284c7" }}>
              <Store size={16} />
            </div>
          </div>
          <div style={{ fontSize: "20px", fontWeight: 800, color: "#0369a1", marginBottom: "2px" }}>
            {marketData ? `₹${marketData.latest_modal_price}` : "Loading..."} <span style={{ fontSize: "11px", fontWeight: 500 }}>/Qtl</span>
          </div>
          <div style={{ fontSize: "12px", color: "#0284c7", fontWeight: 600, marginBottom: "8px" }}>
            {marketData ? marketData.trend_direction : "Live Price Trends"}
          </div>
          <div style={{ fontSize: "11px", color: "#0284c7", fontWeight: 700, display: "flex", alignItems: "center", gap: "4px" }}>
            Where to Sell <ArrowRight size={12} />
          </div>
        </div>

        {/* Card 4: Government Support */}
        <div className="card" onClick={() => setActiveTab("schemes")} style={{ background: "linear-gradient(135deg, #ffffff 0%, #faf5ff 100%)", border: "1px solid #e9d5ff", cursor: "pointer" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
            <span style={{ fontSize: "11px", fontWeight: 700, color: "#6b21a8", textTransform: "uppercase" }}>Govt Subsidy</span>
            <div style={{ background: "#f3e8ff", padding: "5px", borderRadius: "6px", color: "#7c3aed" }}>
              <Landmark size={16} />
            </div>
          </div>
          <div style={{ fontSize: "17px", fontWeight: 800, color: "#6b21a8", marginBottom: "2px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
            {topSchemes.length > 0 ? topSchemes[0].short_name : "PM-KISAN"}
          </div>
          <div style={{ fontSize: "12px", color: "#7c3aed", fontWeight: 600, marginBottom: "8px" }}>
            {topSchemes.length > 0 ? `${(topSchemes[0].match_score * 100).toFixed(0)}% Profile Match` : "Eligible Subsidy"}
          </div>
          <div style={{ fontSize: "11px", color: "#7c3aed", fontWeight: 700, display: "flex", alignItems: "center", gap: "4px" }}>
            View Schemes <ArrowRight size={12} />
          </div>
        </div>
      </div>

      {/* 5. Field Photos History (If any captured) */}
      {fieldPhotos.length > 0 && (
        <div className="card" style={{ marginBottom: "24px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
              <ImageIcon size={16} color="#059669" />
              <h3 style={{ fontSize: "15px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
                Field Photos & Crop Observations
              </h3>
            </div>
            <span style={{ fontSize: "11px", color: "#64748b" }}>{fieldPhotos.length} Photo{fieldPhotos.length > 1 ? "s" : ""}</span>
          </div>

          <div style={{ display: "flex", gap: "10px", overflowX: "auto", paddingBottom: "6px" }}>
            {fieldPhotos.map((photo) => (
              <div key={photo.id} style={{ flexShrink: 0, width: "100px", borderRadius: "8px", overflow: "hidden", border: "1px solid #e2e8f0" }}>
                <img src={photo.url} alt="Field" style={{ width: "100%", height: "80px", objectFit: "cover" }} />
                <div style={{ padding: "4px", fontSize: "10px", textAlign: "center", background: "#f8fafc", color: "#64748b" }}>
                  {photo.time || photo.date}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 6. Main 2-Column Dashboard Sections */}
      <div className="grid-2" style={{ marginBottom: "24px" }}>
        {/* Left Column: Farm Health & Soil Status */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px" }}>
            <h3 style={{ fontSize: "15px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
              🌾 Farm Health & Soil Nutrients
            </h3>
            <span className="badge badge-green">N-P-K Status</span>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginBottom: "14px" }}>
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", fontWeight: 600, marginBottom: "4px" }}>
                <span>Nitrogen (N: {profile.nitrogen} kg/ha)</span>
                <span style={{ color: "#059669" }}>Optimal</span>
              </div>
              <div style={{ width: "100%", height: "7px", background: "#f1f5f9", borderRadius: "4px", overflow: "hidden" }}>
                <div style={{ width: `${Math.min(100, (profile.nitrogen / 140) * 100)}%`, height: "100%", background: "#10b981" }} />
              </div>
            </div>

            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", fontWeight: 600, marginBottom: "4px" }}>
                <span>Phosphorus (P: {profile.phosphorus} kg/ha)</span>
                <span style={{ color: "#0284c7" }}>Good</span>
              </div>
              <div style={{ width: "100%", height: "7px", background: "#f1f5f9", borderRadius: "4px", overflow: "hidden" }}>
                <div style={{ width: `${Math.min(100, (profile.phosphorus / 100) * 100)}%`, height: "100%", background: "#0284c7" }} />
              </div>
            </div>

            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", fontWeight: 600, marginBottom: "4px" }}>
                <span>Potassium (K: {profile.potassium} kg/ha)</span>
                <span style={{ color: "#d97706" }}>Balanced</span>
              </div>
              <div style={{ width: "100%", height: "7px", background: "#f1f5f9", borderRadius: "4px", overflow: "hidden" }}>
                <div style={{ width: `${Math.min(100, (profile.potassium / 80) * 100)}%`, height: "100%", background: "#f59e0b" }} />
              </div>
            </div>
          </div>

          <div style={{ background: "#f8fafc", padding: "10px 14px", borderRadius: "8px", fontSize: "12px", color: "#475569" }}>
            <strong>Soil:</strong> {profile.soil_type} • <strong>pH:</strong> {profile.soil_ph} • <strong>Irrigation:</strong> {profile.irrigation_source}
          </div>
        </div>

        {/* Right Column: Mandi Intelligence Snapshot */}
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px" }}>
            <h3 style={{ fontSize: "15px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
              📈 Top Mandi Realization
            </h3>
            <span className="badge badge-blue">Mandi Rates</span>
          </div>

          {bestMandi ? (
            <div>
              <div style={{ background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: "10px", padding: "12px 14px", marginBottom: "12px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "4px" }}>
                  <span style={{ fontSize: "15px", fontWeight: 800, color: "#065f46" }}>{bestMandi.market}</span>
                  <span className="badge badge-green">{bestMandi.recommendation_badge}</span>
                </div>
                <div style={{ fontSize: "12px", color: "#1e293b" }}>
                  District: <strong>{bestMandi.district}</strong> ({bestMandi.state})
                </div>
                <div style={{ marginTop: "6px", fontSize: "16px", fontWeight: 800, color: "#0f172a" }}>
                  ₹{bestMandi.avg_modal_price} <span style={{ fontSize: "11px", color: "#64748b", fontWeight: 500 }}>avg modal / Qtl (Peak ₹{bestMandi.max_price_recorded})</span>
                </div>
              </div>
              <p style={{ fontSize: "12px", color: "#475569", margin: 0 }}>
                Selling in <strong>{bestMandi.market}</strong> provides optimal price realization over local intermediaries.
              </p>
            </div>
          ) : (
            <div style={{ padding: "14px", textAlign: "center", color: "#64748b", fontSize: "13px" }}>
              Loading Mandi analytics...
            </div>
          )}

          <button 
            onClick={() => setActiveTab("market")}
            className="btn btn-secondary"
            style={{ width: "100%", marginTop: "12px", fontSize: "12px" }}
          >
            Compare Mandis in {profile.state}
          </button>
        </div>
      </div>
    </div>
  );
}
