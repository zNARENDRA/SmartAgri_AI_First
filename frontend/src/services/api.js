const API_BASE = "/api";

export async function fetchApi(endpoint, options = {}) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });
    if (!res.ok) {
      const errorBody = await res.json().catch(() => ({}));
      throw new Error(errorBody.detail || `API Error: ${res.statusText}`);
    }
    return await res.json();
  } catch (err) {
    console.error(`Error calling ${endpoint}:`, err);
    throw err;
  }
}

// Crop Recommendation
export const predictCrop = (data) =>
  fetchApi("/crop-recommendation/predict", {
    method: "POST",
    body: JSON.stringify(data),
  });

export const getCropMetrics = () =>
  fetchApi("/crop-recommendation/metrics");

// Crop Yield Prediction
export const predictYield = (data) =>
  fetchApi("/yield-prediction/predict", {
    method: "POST",
    body: JSON.stringify(data),
  });

export const getYieldMetrics = () =>
  fetchApi("/yield-prediction/metrics");

// Plant Disease Detection
export async function diagnoseLeafFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  
  const res = await fetch(`${API_BASE}/disease-detection/diagnose`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Diagnosis error`);
  }
  return await res.json();
}

export const diagnoseSampleLeaf = (filename) =>
  fetchApi(`/disease-detection/diagnose-sample?filename=${encodeURIComponent(filename)}`, {
    method: "POST",
  });

export const getDiseaseSamples = () =>
  fetchApi("/disease-detection/samples");

export const getDiseaseClasses = () =>
  fetchApi("/disease-detection/classes");

// Weather & Advisory
export const getWeatherAdvisory = (location = "Nashik, Maharashtra", crop = "General", lat = null, lon = null) => {
  let url = `/weather/advisory?location=${encodeURIComponent(location)}&crop=${encodeURIComponent(crop)}`;
  if (lat && lon) url += `&lat=${lat}&lon=${lon}`;
  return fetchApi(url);
};

export const getCurrentWeather = (location = "", lat = null, lon = null) => {
  let url = `/weather/current?location=${encodeURIComponent(location)}`;
  if (lat && lon) url += `&lat=${lat}&lon=${lon}`;
  return fetchApi(url);
};

// Market Intelligence
export const getMarketFilters = () =>
  fetchApi("/market/filters");

export const getMarketTrends = (commodity, state, district = null, mandi = null) => {
  let url = `/market/trends?commodity=${encodeURIComponent(commodity)}&state=${encodeURIComponent(state)}`;
  if (district && district !== "All") url += `&district=${encodeURIComponent(district)}`;
  if (mandi && mandi !== "All") url += `&mandi=${encodeURIComponent(mandi)}`;
  return fetchApi(url);
};

export const getWhereToSell = (commodity, state) =>
  fetchApi(`/market/where-to-sell?commodity=${encodeURIComponent(commodity)}&state=${encodeURIComponent(state)}`);

// Government Schemes
export const searchSchemes = (query = "", category = "All") => {
  let url = "/schemes/search?";
  if (query) url += `query=${encodeURIComponent(query)}&`;
  if (category && category !== "All") url += `category=${encodeURIComponent(category)}&`;
  return fetchApi(url);
};

export const matchSchemesProfile = (profile) =>
  fetchApi("/schemes/match-profile", {
    method: "POST",
    body: JSON.stringify(profile),
  });

// Farmer Profile
export const getFarmerProfile = () =>
  fetchApi("/profile");

export const updateFarmerProfile = (profile) =>
  fetchApi("/profile", {
    method: "POST",
    body: JSON.stringify(profile),
  });

export const getProfilePresets = () =>
  fetchApi("/profile/presets");

export const loadProfilePreset = (presetId) =>
  fetchApi(`/profile/presets/${presetId}`, {
    method: "POST",
  });

// AI Assistant
export const askAssistant = (message, history = [], farmerProfile = null) =>
  fetchApi("/assistant/chat", {
    method: "POST",
    body: JSON.stringify({ message, history, farmer_profile: farmerProfile }),
  });

// Consolidated Farm Action Plan
export const getFarmActionPlan = () =>
  fetchApi("/action-plan/generate");

export const generateCustomActionPlan = (profile) =>
  fetchApi("/action-plan/generate", {
    method: "POST",
    body: JSON.stringify(profile),
  });

// Model & Dataset Information
export const getModelsSummary = () =>
  fetchApi("/models-info/summary");

export const getDataRegistry = () =>
  fetchApi("/models-info/registry");
