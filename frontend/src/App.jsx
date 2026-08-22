import React from "react";
import { FarmerProvider, useFarmer } from "./context/FarmerContext";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import BottomNav from "./components/BottomNav";
import MobileDrawer from "./components/MobileDrawer";
import PlantCameraScanner from "./components/PlantCameraScanner";
import DemoTourModal from "./components/DemoTourModal";
import ActionPlanModal from "./components/ActionPlanModal";

// Pages
import LandingPage from "./pages/LandingPage";
import Dashboard from "./pages/Dashboard";
import CropAdvisor from "./pages/CropAdvisor";
import YieldPredictor from "./pages/YieldPredictor";
import DiseaseDetection from "./pages/DiseaseDetection";
import WeatherAdvisory from "./pages/WeatherAdvisory";
import MarketIntelligence from "./pages/MarketIntelligence";
import GovernmentSchemes from "./pages/GovernmentSchemes";
import AIAssistant from "./pages/AIAssistant";
import FarmerProfile from "./pages/FarmerProfile";
import ModelEvaluationInfo from "./pages/ModelEvaluationInfo";

function MainApp() {
  const useFarmerContextInApp = useFarmer();
  const { activeTab } = useFarmerContextInApp;

  const renderActivePage = () => {
    switch (activeTab) {
      case "landing":
        return <LandingPage />;
      case "dashboard":
        return <Dashboard />;
      case "crop-advisor":
        return <CropAdvisor />;
      case "yield-predictor":
        return <YieldPredictor />;
      case "disease-detection":
        return <DiseaseDetection />;
      case "weather":
        return <WeatherAdvisory />;
      case "market":
        return <MarketIntelligence />;
      case "schemes":
        return <GovernmentSchemes />;
      case "assistant":
        return <AIAssistant />;
      case "profile":
        return <FarmerProfile />;
      case "models-info":
        return <ModelEvaluationInfo />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="app-container">
      {/* Desktop Sidebar */}
      <Sidebar />

      {/* Main Responsive Content Area */}
      <div className="main-content">
        <Navbar />
        <main className="main-viewport">{renderActivePage()}</main>
      </div>

      {/* Mobile-Only Bottom Navigation */}
      <BottomNav />

      {/* Mobile Slide-out Drawer */}
      <MobileDrawer />

      {/* Camera Leaf Scanner Modal */}
      <PlantCameraScanner onScanComplete={(res, img) => {
        useFarmerContextInApp.setGlobalDiseaseResult(res);
        useFarmerContextInApp.setGlobalDiseaseImage(img);
      }} />

      {/* Global Modals */}
      <DemoTourModal />
      <ActionPlanModal />
    </div>
  );
}

export default function App() {
  return (
    <FarmerProvider>
      <MainApp />
    </FarmerProvider>
  );
}
