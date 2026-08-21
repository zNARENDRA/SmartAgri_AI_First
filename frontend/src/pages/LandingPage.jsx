import React from "react";
import { useFarmer } from "../context/FarmerContext";
import {
  Sprout,
  TrendingUp,
  Bug,
  CloudSun,
  Store,
  Landmark,
  BotMessageSquare,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Layers,
  BarChart3,
  Award,
  Camera,
  Activity
} from "lucide-react";

export default function LandingPage() {
  const { setActiveTab, setShowDemoTour } = useFarmer();

  const workflowSteps = [
    {
      num: "01",
      title: "Soil & Agro-Climate Matching",
      desc: "Analyze your farm's N-P-K nutrient profile, pH, and rainfall to discover the most profitable and high-yielding crops.",
      tab: "crop-advisor"
    },
    {
      num: "02",
      title: "Harvest & Yield Forecasting",
      desc: "Calculate expected acreage production, tons per hectare, and customized fertilization strategies before sowing.",
      tab: "yield-predictor"
    },
    {
      num: "03",
      title: "AI Camera Plant Health Scanner",
      desc: "Instantly scan crop leaves using your smartphone camera for rapid detection of fungal and bacterial infections with bio-cures.",
      tab: "disease-detection"
    },
    {
      num: "04",
      title: "Mandi Price Intelligence & Schemes",
      desc: "Compare wholesale APMC mandi rates across districts to know where to sell, and discover matching central/state subsidies.",
      tab: "market"
    }
  ];

  const features = [
    { icon: Sprout, title: "AI Crop Advisor", desc: "Scientific crop selection matching soil N-P-K, pH, temperature, humidity, and rainfall parameters.", tab: "crop-advisor" },
    { icon: TrendingUp, title: "Yield Prediction", desc: "Multi-factor forecasting calculating expected tons per hectare and productivity optimization tips.", tab: "yield-predictor" },
    { icon: Bug, title: "Leaf Disease Detection", desc: "Computer vision diagnosis of 27 plant conditions with biological, organic, and chemical remedies.", tab: "disease-detection" },
    { icon: CloudSun, title: "Weather Agro-Advisory", desc: "Actionable meteorological rules: irrigation schedules, spray safety windows, and frost/heat alerts.", tab: "weather" },
    { icon: Store, title: "Mandi Market Intelligence", desc: "Real-time historical trends, price volatility indices, and 'Where Should I Sell?' market rankings.", tab: "market" },
    { icon: Landmark, title: "Government Scheme Discovery", desc: "Personalized subsidy finder linking farmers directly to verified official MyScheme.gov.in portals.", tab: "schemes" },
  ];

  return (
    <div className="page-wrapper">
      {/* Hero Section */}
      <section style={{
        background: "linear-gradient(135deg, #064e3b 0%, #047857 50%, #065f46 100%)",
        color: "#ffffff",
        borderRadius: "24px",
        padding: "48px 40px",
        marginBottom: "36px",
        boxShadow: "0 20px 30px -10px rgba(4, 120, 87, 0.4)",
        position: "relative",
        overflow: "hidden"
      }}>
        <div style={{ position: "relative", zIndex: 2, maxWidth: "800px" }}>
          <div style={{ display: "inline-flex", alignItems: "center", gap: "8px", background: "rgba(255,255,255,0.15)", border: "1px solid rgba(255,255,255,0.25)", padding: "6px 14px", borderRadius: "9999px", fontSize: "13px", fontWeight: 600, marginBottom: "20px", backdropFilter: "blur(8px)" }}>
            <Sparkles size={14} color="#fde047" />
            <span>Unified Agricultural Decision Support Platform</span>
          </div>

          <h1 style={{ fontSize: "40px", fontWeight: 800, lineHeight: 1.15, letterSpacing: "-0.03em", marginBottom: "16px" }}>
            AI-Powered Farming Decisions for Every Indian Farmer
          </h1>

          <p style={{ fontSize: "16px", color: "#d1fae5", lineHeight: 1.6, marginBottom: "28px", maxWidth: "680px" }}>
            Connecting <strong>Soil Nutrients • Live Weather • Crop Advisory • Plant Leaf Health • Mandi Prices • Government Subsidies</strong> into one simple, actionable assistant for your farm.
          </p>

          <div style={{ display: "flex", flexWrap: "wrap", gap: "14px" }}>
            <button
              onClick={() => setActiveTab("dashboard")}
              className="btn btn-amber"
              style={{ padding: "12px 24px", fontSize: "15px", fontWeight: 700 }}
            >
              <span>Open Farmer Dashboard</span>
              <ArrowRight size={18} />
            </button>

            <button
              onClick={() => setActiveTab("assistant")}
              className="btn"
              style={{ background: "rgba(255,255,255,0.15)", color: "#ffffff", border: "1px solid rgba(255,255,255,0.3)", padding: "12px 20px", fontSize: "15px" }}
            >
              <BotMessageSquare size={18} />
              <span>Talk to AI Assistant</span>
            </button>

            <button
              onClick={() => setShowDemoTour(true)}
              className="btn"
              style={{ background: "#ffffff", color: "#065f46", padding: "12px 20px", fontSize: "15px", fontWeight: 700 }}
            >
              <Award size={18} color="#d97706" />
              <span>Interactive Platform Tour</span>
            </button>
          </div>
        </div>
      </section>

      {/* 4-Step Smart Farming Decision Journey */}
      <section style={{ marginBottom: "40px" }}>
        <div style={{ marginBottom: "20px" }}>
          <h2 style={{ fontSize: "22px", fontWeight: 800, color: "#0f172a", margin: 0 }}>
            How SmartAgri AI Empowers Your Farm
          </h2>
          <p style={{ fontSize: "13px", color: "#64748b", marginTop: "4px" }}>
            A complete decision workflow from soil preparation to market realization.
          </p>
        </div>

        <div className="grid-4">
          {workflowSteps.map((s, i) => (
            <div
              key={i}
              className="card"
              onClick={() => setActiveTab(s.tab)}
              style={{
                cursor: "pointer",
                borderTop: "4px solid #059669",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                padding: "20px"
              }}
            >
              <div>
                <span style={{ fontSize: "12px", fontWeight: 800, color: "#059669", letterSpacing: "0.05em" }}>
                  STEP {s.num}
                </span>
                <h3 style={{ fontSize: "15px", fontWeight: 800, color: "#0f172a", margin: "6px 0 8px 0" }}>
                  {s.title}
                </h3>
                <p style={{ fontSize: "12px", color: "#475569", lineHeight: 1.5, margin: 0 }}>
                  {s.desc}
                </p>
              </div>

              <div style={{ marginTop: "14px", display: "flex", alignItems: "center", gap: "4px", fontSize: "12px", fontWeight: 700, color: "#059669" }}>
                <span>Try Feature</span>
                <ArrowRight size={12} />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Core Capabilities Grid */}
      <section style={{ marginBottom: "40px" }}>
        <div style={{ textAlign: "center", maxWidth: "600px", margin: "0 auto 28px" }}>
          <h2 style={{ fontSize: "26px", fontWeight: 800, color: "#0f172a", letterSpacing: "-0.02em" }}>
            Comprehensive Multi-Module AI Tools
          </h2>
          <p style={{ fontSize: "14px", color: "#64748b" }}>
            Designed specifically to solve real-world agricultural challenges with precision and simplicity.
          </p>
        </div>

        <div className="grid-3">
          {features.map((f, idx) => {
            const Icon = f.icon;
            return (
              <div 
                key={idx} 
                className="card"
                onClick={() => setActiveTab(f.tab)}
                style={{ cursor: "pointer", display: "flex", flexDirection: "column", justifyContent: "space-between" }}
              >
                <div>
                  <div style={{
                    width: "44px",
                    height: "44px",
                    borderRadius: "12px",
                    background: "#f0fdf4",
                    color: "#059669",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    marginBottom: "16px"
                  }}>
                    <Icon size={22} />
                  </div>
                  <h3 style={{ fontSize: "17px", fontWeight: 700, color: "#0f172a", marginBottom: "8px" }}>
                    {f.title}
                  </h3>
                  <p style={{ fontSize: "13px", color: "#475569", lineHeight: 1.5, marginBottom: "16px" }}>
                    {f.desc}
                  </p>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "6px", fontSize: "13px", fontWeight: 600, color: "#059669" }}>
                  <span>Open Tool</span>
                  <ArrowRight size={14} />
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Safety and Ethical Advisory Safeguards */}
      <section style={{
        background: "#f8fafc",
        border: "1px solid #e2e8f0",
        borderRadius: "16px",
        padding: "24px 30px",
        display: "flex",
        alignItems: "center",
        gap: "20px"
      }}>
        <div style={{ background: "#e0f2fe", color: "#0369a1", padding: "12px", borderRadius: "12px", flexShrink: 0 }}>
          <ShieldCheck size={28} />
        </div>
        <div>
          <h4 style={{ fontSize: "15px", fontWeight: 700, color: "#0f172a", marginBottom: "4px" }}>
            Production Reliability & Ethical AI Safeguards
          </h4>
          <p style={{ fontSize: "13px", color: "#64748b", margin: 0, lineHeight: 1.5 }}>
            Our platform provides decision support with transparent confidence metrics and feature analysis. We never make unsubstantiated guarantee claims regarding crop yields, disease cures, or government eligibility. Farmers are provided direct verified links to official portals (MyScheme.gov.in) and local Krishi Vigyan Kendra contacts.
          </p>
        </div>
      </section>
    </div>
  );
}
