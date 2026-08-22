import React, { createContext, useContext, useState, useEffect } from "react";
import { 
  getFarmerProfile, 
  updateFarmerProfile, 
  getProfilePresets, 
  loadProfilePreset, 
  getWeatherAdvisory, 
  getFarmActionPlan 
} from "../services/api";

const FarmerContext = createContext();

export function FarmerProvider({ children }) {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [profile, setProfile] = useState({
    name: "Ramesh Patil",
    state: "Maharashtra",
    district: "Nashik",
    village: "Niphad",
    land_size_acres: 3.5,
    soil_type: "Black Soil (Regur)",
    soil_ph: 6.8,
    nitrogen: 75.0,
    phosphorus: 45.0,
    potassium: 40.0,
    current_crop: "Soybean",
    farming_season: "Kharif",
    irrigation_source: "Drip Irrigation & Well",
    farmer_category: "Small (1-2 ha)",
  });
  
  const [presets, setPresets] = useState([]);
  const [weather, setWeather] = useState(null);
  const [actionPlan, setActionPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // Navigation & Modal States
  const [showDemoTour, setShowDemoTour] = useState(false);
  const [showActionPlanModal, setShowActionPlanModal] = useState(false);
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);
  const [showCameraScanner, setShowCameraScanner] = useState(false);
  
  // Cross-module Context Bridge for AI Assistant
  const [pendingAiContext, setPendingAiContext] = useState(null);
  
  // Global Disease Detection state bridge (from Scanner to Disease Tab)
  const [globalDiseaseResult, setGlobalDiseaseResult] = useState(null);
  const [globalDiseaseImage, setGlobalDiseaseImage] = useState(null);
  
  // Field Photos (Visual Context History)
  const [fieldPhotos, setFieldPhotos] = useState([]);

  // Fetch initial profile, presets, weather, action plan
  useEffect(() => {
    async function initData() {
      try {
        const p = await getFarmerProfile();
        setProfile(p);
        
        const pr = await getProfilePresets();
        setPresets(pr);
        
        const w = await getWeatherAdvisory(p.district || p.state, p.current_crop);
        setWeather(w);
      } catch (e) {
        console.error("Context init error:", e);
      }
    }
    initData();
  }, []);

  const saveProfile = async (newProfile) => {
    setLoading(true);
    try {
      const updated = await updateFarmerProfile(newProfile);
      setProfile(updated);
      const w = await getWeatherAdvisory(updated.district || updated.state, updated.current_crop);
      setWeather(w);
    } catch (e) {
      console.error("Failed to update profile:", e);
    } finally {
      setLoading(false);
    }
  };

  const applyPreset = async (presetId) => {
    setLoading(true);
    try {
      const updated = await loadProfilePreset(presetId);
      setProfile(updated);
      const w = await getWeatherAdvisory(updated.district || updated.state, updated.current_crop);
      setWeather(w);
    } catch (e) {
      console.error("Failed to load preset:", e);
    } finally {
      setLoading(false);
    }
  };

  const refreshActionPlan = async () => {
    try {
      const plan = await getFarmActionPlan();
      setActionPlan(plan);
      return plan;
    } catch (e) {
      console.error("Failed to refresh action plan:", e);
      return null;
    }
  };

  // Bridge disease or field photo into AI Assistant
  const askAiAboutDisease = (diseaseResult, imagePreviewUrl) => {
    setPendingAiContext({
      type: "disease",
      crop: diseaseResult.detected_crop,
      condition: diseaseResult.condition,
      status: diseaseResult.status,
      confidence: diseaseResult.confidence_percentage,
      severity: diseaseResult.severity,
      symptoms: diseaseResult.symptoms,
      organicTreatment: diseaseResult.organic_treatment,
      chemicalTreatment: diseaseResult.chemical_treatment,
      prevention: diseaseResult.prevention_measures,
      imageUrl: imagePreviewUrl
    });
    setActiveTab("assistant");
  };

  const addFieldPhoto = (photoDataUrl) => {
    const newPhoto = {
      id: Date.now(),
      url: photoDataUrl,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      date: new Date().toLocaleDateString([], { month: 'short', day: 'numeric' })
    };
    setFieldPhotos((prev) => [newPhoto, ...prev]);
    return newPhoto;
  };

  return (
    <FarmerContext.Provider
      value={{
        activeTab,
        setActiveTab,
        profile,
        setProfile,
        saveProfile,
        presets,
        applyPreset,
        weather,
        actionPlan,
        refreshActionPlan,
        loading,
        showDemoTour,
        setShowDemoTour,
        showActionPlanModal,
        setShowActionPlanModal,
        mobileDrawerOpen,
        setMobileDrawerOpen,
        showCameraScanner,
        setShowCameraScanner,
        pendingAiContext,
        setPendingAiContext,
        askAiAboutDisease,
        fieldPhotos,
        addFieldPhoto,
        globalDiseaseResult,
        setGlobalDiseaseResult,
        globalDiseaseImage,
        setGlobalDiseaseImage
      }}
    >
      {children}
    </FarmerContext.Provider>
  );
}

export function useFarmer() {
  return useContext(FarmerContext);
}
