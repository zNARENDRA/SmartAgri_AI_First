import React from "react";
import { useFarmer } from "../context/FarmerContext";
import { 
  Sprout, 
  CloudSun, 
  MapPin, 
  User, 
  Sparkles, 
  FileText,
  PlayCircle,
  Menu,
  Camera
} from "lucide-react";

export default function Navbar() {
  const { 
    profile, 
    weather, 
    setShowDemoTour, 
    setShowActionPlanModal, 
    refreshActionPlan,
    activeTab,
    setActiveTab,
    setMobileDrawerOpen,
    setShowCameraScanner
  } = useFarmer();

  const handleOpenActionPlan = async () => {
    await refreshActionPlan();
    setShowActionPlanModal(true);
  };

  return (
    <header className="top-navbar">
      {/* Left Area: Hamburger (Mobile) + Logo & Title */}
      <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
        {/* Mobile Hamburger Button */}
        <button
          onClick={() => setMobileDrawerOpen(true)}
          className="mobile-hamburger-btn"
          aria-label="Open Navigation Menu"
        >
          <Menu size={22} color="#0f172a" />
        </button>

        {/* App Logo */}
        <div 
          onClick={() => setActiveTab("landing")}
          style={{ 
            display: "flex", 
            alignItems: "center", 
            gap: "8px", 
            cursor: "pointer" 
          }}
        >
          <div style={{
            width: "34px",
            height: "34px",
            borderRadius: "9px",
            background: "linear-gradient(135deg, #059669 0%, #047857 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
            boxShadow: "0 4px 10px rgba(5, 150, 105, 0.25)",
            flexShrink: 0
          }}>
            <Sprout size={20} />
          </div>
          <div>
            <div style={{ fontWeight: 800, fontSize: "16px", letterSpacing: "-0.02em", color: "#0f172a", lineHeight: 1.1 }}>
              SmartAgri <span style={{ color: "#059669" }}>AI</span>
            </div>
            <div className="navbar-subtitle-hide" style={{ fontSize: "10px", color: "#64748b", fontWeight: 500 }}>
              AI Platform for Farmers
            </div>
          </div>
        </div>

        {/* Location & Weather Pill (Responsive) */}
        {weather && (
          <div 
            onClick={() => setActiveTab("weather")}
            className="navbar-weather-pill"
          >
            <MapPin size={12} color="#059669" />
            <span>{profile.district || profile.state}</span>
            <span style={{ color: "#86efac" }}>•</span>
            <CloudSun size={13} color="#059669" />
            <span>{weather.current.temperature.toFixed(0)}°C</span>
          </div>
        )}
      </div>

      {/* Right Area: Actions & Profile */}
      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        {/* Mobile Camera Quick Tap */}
        <button
          onClick={() => setShowCameraScanner(true)}
          className="mobile-camera-quick-btn"
          aria-label="Scan Plant Disease"
          title="Scan Plant Disease"
        >
          <Camera size={18} />
          <span className="mobile-hide-text">Scan</span>
        </button>

        {/* Desktop-only Hackathon Demo Tour Button */}
        <button 
          onClick={() => setShowDemoTour(true)}
          className="btn btn-secondary desktop-only-btn"
          style={{ padding: "7px 12px", fontSize: "12px" }}
        >
          <PlayCircle size={14} color="#059669" />
          <span>Demo Tour</span>
        </button>

        {/* Desktop-only View Action Plan Button */}
        <button 
          onClick={handleOpenActionPlan}
          className="btn btn-amber desktop-only-btn"
          style={{ padding: "7px 14px", fontSize: "12px" }}
        >
          <FileText size={14} />
          <span>Action Plan</span>
        </button>

        {/* Active Profile Pill */}
        <div 
          onClick={() => setActiveTab("profile")}
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            padding: "4px 10px",
            background: "#f8fafc",
            border: "1px solid #e2e8f0",
            borderRadius: "8px",
            cursor: "pointer",
            minHeight: "36px"
          }}
        >
          <div style={{
            width: "26px",
            height: "26px",
            borderRadius: "50%",
            background: "#0284c7",
            color: "#ffffff",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "11px",
            fontWeight: 700,
            flexShrink: 0
          }}>
            {profile.name.charAt(0)}
          </div>
          <div className="navbar-profile-text" style={{ textAlign: "left", lineHeight: 1.1 }}>
            <div style={{ fontSize: "12px", fontWeight: 700, color: "#1e293b", whiteSpace: "nowrap" }}>
              {profile.name.split(" ")[0]}
            </div>
            <div style={{ fontSize: "9px", color: "#64748b" }}>
              {profile.land_size_acres} Ac
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
