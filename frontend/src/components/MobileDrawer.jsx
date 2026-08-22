import React from "react";
import { useFarmer } from "../context/FarmerContext";
import {
  X,
  LayoutDashboard,
  Sprout,
  TrendingUp,
  Bug,
  CloudSun,
  Store,
  Landmark,
  BotMessageSquare,
  UserCheck,
  Info,
  FileCheck2,
  HelpCircle,
  Camera,
  MapPin
} from "lucide-react";

export default function MobileDrawer() {
  const {
    activeTab,
    setActiveTab,
    profile,
    mobileDrawerOpen,
    setMobileDrawerOpen,
    setShowActionPlanModal,
    setShowDemoTour,
    setShowCameraScanner,
    refreshActionPlan
  } = useFarmer();

  if (!mobileDrawerOpen) return null;

  const handleNav = (tabId) => {
    setActiveTab(tabId);
    setMobileDrawerOpen(false);
  };

  const navItems = [
    { id: "dashboard", label: "Farmer Dashboard", icon: LayoutDashboard },
    { id: "crop-advisor", label: "AI Crop Advisor", icon: Sprout },
    { id: "yield-predictor", label: "Crop Yield Prediction", icon: TrendingUp },
    { id: "disease-detection", label: "Leaf Disease Detection", icon: Bug },
    { id: "weather", label: "Weather & Advisory", icon: CloudSun },
    { id: "market", label: "Mandi Market Intelligence", icon: Store },
    { id: "schemes", label: "Government Schemes", icon: Landmark },
    { id: "assistant", label: "AI Farmer Assistant", icon: BotMessageSquare },
    { id: "profile", label: "Farmer Profile & Presets", icon: UserCheck },
    { id: "models-info", label: "About & Technology", icon: Info }
  ];

  return (
    <div className="mobile-drawer-overlay" onClick={() => setMobileDrawerOpen(false)}>
      <div className="mobile-drawer-content" onClick={(e) => e.stopPropagation()}>
        {/* Drawer Header */}
        <div className="mobile-drawer-header">
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <div className="mobile-drawer-avatar">
              {profile.name ? profile.name[0] : "K"}
            </div>
            <div>
              <div style={{ fontSize: "16px", fontWeight: 800, color: "#0f172a" }}>
                {profile.name}
              </div>
              <div style={{ fontSize: "12px", color: "#64748b", display: "flex", alignItems: "center", gap: "4px" }}>
                <MapPin size={12} /> {profile.district}, {profile.state}
              </div>
            </div>
          </div>

          <button
            onClick={() => setMobileDrawerOpen(false)}
            className="mobile-drawer-close"
            aria-label="Close Navigation Menu"
          >
            <X size={20} />
          </button>
        </div>

        {/* Quick Camera Action Banner */}
        <div style={{ padding: "12px 16px 4px 16px" }}>
          <button
            onClick={() => {
              setMobileDrawerOpen(false);
              setShowCameraScanner(true);
            }}
            className="btn btn-primary"
            style={{ width: "100%", padding: "12px", fontSize: "14px", justifyContent: "center" }}
          >
            <Camera size={18} />
            <span>Open Camera Leaf Scanner</span>
          </button>
        </div>

        {/* Navigation List */}
        <div className="mobile-drawer-body">
          <div style={{ fontSize: "11px", fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", padding: "10px 16px 4px 16px" }}>
            All Modules & Tools
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleNav(item.id)}
                className={`mobile-drawer-item ${isActive ? "active" : ""}`}
              >
                <Icon size={18} className="mobile-drawer-icon" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

        {/* Drawer Footer Actions */}
        <div className="mobile-drawer-footer">
          <button
            onClick={async () => {
              setMobileDrawerOpen(false);
              await refreshActionPlan();
              setShowActionPlanModal(true);
            }}
            className="btn btn-amber"
            style={{ width: "100%", padding: "10px", fontSize: "13px", justifyContent: "center" }}
          >
            <FileCheck2 size={16} />
            <span>View Farm Action Plan</span>
          </button>

          <button
            onClick={() => {
              setMobileDrawerOpen(false);
              setShowDemoTour(true);
            }}
            className="btn btn-secondary"
            style={{ width: "100%", padding: "10px", fontSize: "13px", justifyContent: "center" }}
          >
            <HelpCircle size={16} />
            <span>Interactive Demo Tour</span>
          </button>
        </div>
      </div>
    </div>
  );
}
