from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# ----------------- Farmer Profile -----------------
class FarmerProfile(BaseModel):
    name: str = Field(default="Ramesh Kumar", description="Farmer full name")
    state: str = Field(default="Maharashtra", description="State in India")
    district: str = Field(default="Nashik", description="District")
    village: Optional[str] = Field(default="Niphad", description="Village")
    land_size_acres: float = Field(default=3.5, description="Land size in acres")
    soil_type: str = Field(default="Black Soil (Regur)", description="Soil classification")
    soil_ph: float = Field(default=6.8, description="Soil pH level (3.5 - 9.5)")
    nitrogen: float = Field(default=75.0, description="Nitrogen content (N in kg/ha)")
    phosphorus: float = Field(default=45.0, description="Phosphorus content (P in kg/ha)")
    potassium: float = Field(default=40.0, description="Potassium content (K in kg/ha)")
    current_crop: Optional[str] = Field(default="Soybean", description="Currently planted crop")
    farming_season: str = Field(default="Kharif", description="Current farming season")
    irrigation_source: str = Field(default="Drip Irrigation & Well", description="Irrigation facility")
    farmer_category: str = Field(default="Small (1-2 ha)", description="Farmer classification")

# ----------------- Crop Recommendation -----------------
class CropRecommendationRequest(BaseModel):
    N: float = Field(..., ge=0, le=250, description="Nitrogen in soil (kg/ha)")
    P: float = Field(..., ge=0, le=250, description="Phosphorus in soil (kg/ha)")
    K: float = Field(..., ge=0, le=300, description="Potassium in soil (kg/ha)")
    temperature: float = Field(..., ge=0, le=55, description="Ambient temperature (°C)")
    humidity: float = Field(..., ge=5, le=100, description="Relative humidity (%)")
    ph: float = Field(..., ge=3.5, le=10.0, description="Soil pH value")
    rainfall: float = Field(..., ge=0, le=600, description="Rainfall (mm)")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of top crops to return")
    state: Optional[str] = Field(default="Maharashtra", description="State for district historical context")

class CropScore(BaseModel):
    crop: str
    confidence: float
    percentage: str
    soil_suitability: str
    key_advantages: List[str]
    water_requirement: str
    expected_duration_days: str

class CropRecommendationResponse(BaseModel):
    top_crop: str
    recommendations: List[CropScore]
    feature_importances: Dict[str, float]
    input_parameters: Dict[str, Any]
    nutritional_analysis: Dict[str, str]
    district_context: Optional[Dict[str, Any]] = None
    disclaimer: str

# ----------------- Crop Yield Prediction -----------------
class YieldPredictionRequest(BaseModel):
    crop: str = Field(..., description="Crop name (e.g., Rice, Wheat, Cotton)")
    state: str = Field(..., description="State in India")
    season: str = Field(..., description="Season (Kharif, Rabi, Summer, Whole Year)")
    area: float = Field(..., gt=0, description="Area in Hectares")
    annual_rainfall: float = Field(default=1050.0, ge=100, le=4000, description="Annual rainfall (mm)")
    fertilizer: float = Field(default=110.0, ge=10, le=500, description="Fertilizer consumption (kg/ha)")
    pesticide: float = Field(default=1.5, ge=0.0, le=15.0, description="Pesticide consumption (kg/ha)")

class YieldPredictionResponse(BaseModel):
    crop: str
    predicted_yield_tons_per_ha: float
    predicted_yield_quintals_per_acre: float
    total_expected_production_tons: float
    yield_range_min_tons_per_ha: float
    yield_range_max_tons_per_ha: float
    productivity_rating: str
    key_drivers: Dict[str, float]
    optimization_recommendations: List[str]
    model_evaluation: Optional[Dict[str, Any]] = None
    climate_risk_index: Optional[Dict[str, Any]] = None
    disclaimer: str

# ----------------- Plant Disease Detection -----------------
class DiseaseDiagnosisResponse(BaseModel):
    request_id: Optional[str] = Field(default="DX-2026-0001", description="Unique diagnostic request ID")
    is_low_confidence: bool = Field(default=False, description="True if prediction confidence is below threshold (< 40%)")
    confidence_tier: str = Field(default="High Confidence", description="High Confidence, Moderate Confidence, or Low Confidence / Uncertain")
    detected_crop: str
    condition: str
    status: str # Healthy, Diseased, or Uncertain
    severity: str # None, Low, Moderate, High, Severe, or Uncertain
    confidence: float
    confidence_percentage: str
    pathogen: str
    symptoms: str
    immediate_actions: str
    organic_treatment: str
    chemical_treatment: str
    prevention_measures: str
    top_predictions: List[Dict[str, Any]]
    disclaimer: str
    debug_info: Optional[Dict[str, Any]] = None

# ----------------- Weather & Advisory -----------------
class WeatherCurrent(BaseModel):
    temperature: float
    humidity: float
    wind_speed_kmh: float
    precipitation_mm: float
    condition_text: str
    weather_code: int
    location_name: str

class DailyForecastItem(BaseModel):
    date: str
    day_name: str
    temp_max: float
    temp_min: float
    rain_sum_mm: float
    precipitation_probability_max: int
    condition_text: str
    weather_code: int

class AgroAdvisory(BaseModel):
    irrigation_advice: Dict[str, Any]
    spraying_window: Dict[str, Any]
    heat_cold_stress: Dict[str, Any]
    pest_disease_risk: Dict[str, Any]
    harvest_recommendation: Dict[str, Any]
    overall_farm_alert: str

class WeatherAdvisoryResponse(BaseModel):
    current: WeatherCurrent
    forecast: List[DailyForecastItem]
    advisory: AgroAdvisory
    imd_rainfall_baseline: Optional[Dict[str, Any]] = None
    provider: str

# ----------------- Market Intelligence -----------------
class MarketFilterOptions(BaseModel):
    states: List[str]
    districts_by_state: Dict[str, List[str]]
    mandis_by_district: Dict[str, List[str]]
    commodities: List[str]

class PriceTrendPoint(BaseModel):
    date: str
    min_price: int
    max_price: int
    modal_price: int

class MarketTrendResponse(BaseModel):
    commodity: str
    state: str
    district: Optional[str]
    mandi: Optional[str]
    latest_modal_price: int
    min_price: int
    max_price: int
    average_price: float
    price_change_percentage: float
    trend_direction: str # "Rising", "Falling", "Stable"
    volatility_rating: str # "Low", "Moderate", "High"
    price_history: List[PriceTrendPoint]
    data_attribution: str

class MandiRankItem(BaseModel):
    rank: int
    market: str
    district: str
    state: str
    avg_modal_price: float
    latest_price: int
    max_price_recorded: int
    volatility_std: float
    recommendation_badge: str

class WhereToSellResponse(BaseModel):
    commodity: str
    state: str
    best_mandis: List[MandiRankItem]
    price_spread_analysis: str
    market_advice: str
    data_attribution: str

# ----------------- Government Schemes -----------------
class SchemeItem(BaseModel):
    id: str
    scheme_name: str
    short_name: str
    category: str
    sponsoring_agency: str
    level: str
    target_beneficiaries: str
    description: str
    benefits: str
    eligibility_criteria: Dict[str, Any]
    documents_required: List[str]
    application_process: str
    official_url: str
    myscheme_url: str
    match_score: Optional[float] = None
    match_reasons: Optional[List[str]] = None

class SchemeSearchResponse(BaseModel):
    total_schemes: int
    results: List[SchemeItem]
    categories: List[str]
    disclaimer: str

# ----------------- AI Assistant -----------------
class ChatMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None

class AssistantQueryRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []
    farmer_profile: Optional[FarmerProfile] = None

class AssistantQueryResponse(BaseModel):
    reply: str
    detected_intent: str
    tools_used: List[str]
    structured_data: Optional[Dict[str, Any]] = None
    suggested_followups: List[str]

# ----------------- Farm Action Plan -----------------
class FarmActionPlanResponse(BaseModel):
    farmer_name: str
    generated_at: str
    crop_advice: Dict[str, Any]
    irrigation_water_advice: Dict[str, Any]
    weather_action: Dict[str, Any]
    crop_health_action: Dict[str, Any]
    market_advice: Dict[str, Any]
    government_support: Dict[str, Any]
    critical_risks: List[str]
    immediate_next_steps: List[str]
    disclaimer: str
