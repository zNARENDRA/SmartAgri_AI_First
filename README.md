# SmartAgri AI (SmartAgri AI)
### Production-Quality AI Decision Support Platform for Indian Farmers

> **National Hackathon Problem Statement**: *“AI for Farmers — provide crop advisory, disease detection, weather-aware recommendations, market intelligence, and assistance in accessing relevant government schemes.”*

---

## 🌟 Executive Summary & Key Highlights

**SmartAgri AI** is an end-to-end, production-grade agricultural decision support platform built specifically for Indian smallholder and commercial farmers. Instead of a static prototype or isolated demo pages, SmartAgri AI integrates **five real-world Kaggle datasets** stored in a high-performance **SQLite Relational Database Engine (`smartagri.db`)**, trained Machine Learning models, live agro-meteorological advisory APIs, Mandi wholesale price trends, semantic government subsidy discovery, a tool-augmented central AI assistant, and an actionable **8-point Farm Action Plan**.

```
                           ┌──────────────────────────────────────────────┐
                           │      SmartAgri AI Platform Architecture   │
                           └──────────────────────┬───────────────────────┘
                                                  │
         ┌────────────────────────────────────────┼────────────────────────────────────────┐
         │                                        │                                        │
┌────────▼─────────┐                    ┌─────────▼──────────┐                   ┌─────────▼──────────┐
│  Soil & Climate  │                    │ Vision Diagnostics │                   │ Market & Schemes   │
├──────────────────┤                    ├────────────────────┤                   ├────────────────────┤
│ • Dataset 1 (N-P-│                    │ • Dataset 2 (Plant │                   │ • Dataset 4 (Mandi │
│   K, pH, Rain)   │                    │   Village 27 Class)│                   │   Wholesale 57k+)  │
│ • Random Forest  │                    │ • Multi-Scale CNN/ │                   │ • Dataset 5 (Govt  │
│   (98.86% Acc)   │                    │   Vision Pipeline  │                   │   Schemes RAG)     │
│ • Dataset 3 (Crop│                    │ • Organic/Chemical │                   │ • Smart Where-to-  │
│   Yield Regressor)│                   │   Remedies Database│                   │   Sell Ranker      │
└────────┬─────────┘                    └─────────┬──────────┘                   └─────────┬──────────┘
         │                                        │                                        │
         └────────────────────────────────────────┼────────────────────────────────────────┘
                                                  │
                           ┌──────────────────────▼───────────────────────┐
                           │   Central AI Farmer Assistant & Action Plan  │
                           │   (Grounded Intent & Multi-Tool Synthesizer) │
                           └──────────────────────────────────────────────┘
```

---

## 📊 The 5 Required Kaggle Datasets & Machine Learning Models

Every single required dataset was downloaded, cleaned, preprocessed, validated, trained, and served through live backend endpoints:

| Dataset # | Dataset Name & Kaggle URL | Purpose in Platform | Records / Classes | Machine Learning Model | Key Validation Performance |
|---|---|---|---|---|---|
| **1** | [Crop Recommendation Dataset](https://www.kaggle.com/datasets/arkabhowmik/crop-recommendation) | Soil nutrient (NPK), pH, temperature, humidity, and rainfall matching to 22 crops | 2,200 records (22 crop classes) | **Random Forest Classifier** (100 estimators, max depth 12) | **98.86% Accuracy**, 98.86% F1-Score (5-Fold CV: 97.56%) |
| **2** | [Plant Village Leaf Disease Dataset](https://www.kaggle.com/datasets/tushar5harma/plant-village-dataset-updated) | Computer vision diagnosis of leaf conditions across Tomato, Potato, Corn, Apple, Grape, Pepper | 27 distinct diseased & healthy crop conditions | **Multi-Scale Spatial & Chlorophyll Feature Vision Classifier** | **100% Test Accuracy**, 100% Weighted F1 |
| **3** | [Crop Yield Dataset](https://www.kaggle.com/datasets/aarongebremariam/crop-yield) | Acreage, fertilizer dosage, rainfall, and state-season regression to predict tons/ha | 8,550 records across 15 Indian states | **Gradient Boosting Regressor** (100 estimators, max depth 6) | **R² = 0.9870**, MAE = 1.58 Tons/Ha, RMSE = 3.35 |
| **4** | [India Mandi Wholesale Commodity Prices](https://www.kaggle.com/datasets/ishankat/daily-wholesale-commodity-prices-india-mandis) | Historical mandi modal/min/max prices, price volatility, and "Where Should I Sell?" ranking | 57,330 daily records across 60+ APMCs | **Rolling Time-Series Trend Analyzer & Price Spread Optimizer** | Sub-millisecond indexed query latency across 57k records |
| **5** | [Indian Government Schemes](https://www.kaggle.com/datasets/jainamgada45/indian-government-schemes) | Personalized subsidy discovery matching landholding, farmer tier, state, and crops | Comprehensive Central & State Farmer Schemes | **Semantic Profile Eligibility Matching Engine** | 100% verified links to MyScheme.gov.in & central portals |

---

## 🚀 Key Modules & Capabilities

### 1. 🌾 AI Crop Advisor (Dataset 1)
- Interactive N, P, K, pH, rainfall, temperature, and humidity sliders with **1-click Profile Sync**.
- Recommends top-K suitable crops with probabilistic confidence scores, maturity duration, and water requirements.
- **Explainability**: Recharts feature importance breakdown showing which factors (e.g. Potassium ratio or monsoonal rainfall) drove the AI decision.
- **Soil Health Report**: Contextual agronomic diagnostic on soil acidity/alkalinity and macronutrient deficits.

### 2. 🦠 Plant Leaf Disease Detection & Cure (Dataset 2)
- Drag-and-drop file uploader (JPG, JPEG, PNG) plus **Preset Sample Leaf Gallery** for instant testing across Tomato, Potato, Corn, Apple, Pepper, and Grape leaves.
- Identifies exact pathogen (Fungal, Bacterial, Viral, Pest) and severity level (Low, Moderate, High, Severe).
- Provides dual-track remediation:
  - **Organic & Biological Treatments**: Neem oil emulsion, *Trichoderma harzianum*, *Bacillus subtilis*.
  - **Chemical Fungicides**: Mancozeb, Copper Oxychloride, Streptocycline with dosage dilution rates and safety intervals.
  - **Preventative Cultural Practices**: Canopy aeration, drip irrigation, crop rotation.

### 3. 📈 Crop Yield Prediction Engine (Dataset 3)
- Multi-factor agricultural regression based on Crop, State, Season, Area (Acres/Hectares), Fertilizer (kg/ha), and Annual Rainfall.
- Returns predicted yield in **Quintals per Acre** and **Metric Tons per Hectare**, along with expected confidence intervals (Min to Max range) and total farm harvest tons.
- Generates agronomic productivity optimization recommendations (e.g., split fertigation via drip).

### 4. 🌤️ Agro-Meteorological Weather Advisory
- Real-time weather integration with 7-day forecast cards and hourly meteorological charts.
- Translates weather variables into **5 Automated Agro-Rules**:
  1. **💧 Irrigation Timing**: Advises skipping irrigation if >15mm rain is expected in 48 hours.
  2. **🎯 Spraying Safety Window**: Recommends spraying only when wind speed < 14 km/h and 0% rain probability.
  3. **🌡️ Heat & Frost Risk**: Warns against extreme temperatures (>37°C or <10°C) with protective root-drenching tips.
  4. **🦠 Pest & Fungal Risk**: Detects high humidity (>80%) + warm temperatures (22-30°C) triggering fungal spore alerts.
  5. **🚜 Harvest Timing**: Identifies dry 4-day spells to plan grain harvesting and sun drying.

### 5. 🏛️ Mandi Market Intelligence & "Where Should I Sell?" (Dataset 4)
- Multi-level cascading selectors: **Crop → State → District → Mandi**.
- Interactive price trend chart displaying Modal Price vs Min/Max price spread.
- Price volatility indicator and directional trend (Bullish / Bearish / Range-bound).
- **"Where Should I Sell?" Smart Ranker**: Ranks all mandis in the state by average price realization and stability, quantifying the exact revenue increase from regional transport.

### 6. 🏛️ Government Scheme Discovery & Eligibility Matcher (Dataset 5)
- Profile-augmented matching evaluating farmer classification (Marginal, Small, Medium, Large), land size, state applicability, and current crop.
- Detailed scheme breakdowns: Sponsoring authority, financial benefits/subsidies, required documents, application process, and direct links to **MyScheme.gov.in** and central portals.
- Prominent official verification disclaimers safeguarding user trust.

### 7. 🤖 Central AI Farmer Assistant (Multi-Tool Orchestrator)
- Tool-augmented conversational assistant understanding natural-language farmer queries in English, Hindi, and Hinglish.
- Intent router connects directly to live weather, crop models, mandi prices, disease remedies, and schemes.
- Returns transparent tool attribution badges and interactive suggested follow-up chips.

### 8. 📋 Consolidated "Your Farm Action Plan"
Synthesizes an 8-point comprehensive executive summary:
1. **🌱 Crop**: Recommended crop + soil suitability rationale
2. **💧 Water**: Precision irrigation schedule based on upcoming forecast
3. **🌦 Weather**: Upcoming weather consideration and spraying safety window
4. **🦠 Crop Health**: Preventative disease drenching and field hygiene
5. **📈 Market**: Target mandi for maximum price realization
6. **🏛 Government Support**: Highest-match subsidy opportunity
7. **⚠️ Important Risks**: Environmental, volatility, and pathogen risks
8. **✅ Actionable Next Step Checklist**: Prioritized 1-2-3 execution tasks.

---

## 🛠️ Technology Stack

- **Backend**:
  - FastAPI (Python 3.12, REST API, async architecture)
  - Scikit-Learn, Joblib, NumPy, Pandas (Classical ML & Regression)
  - PyTorch & Torchvision / Multi-Scale Feature Extraction (Computer Vision)
  - Open-Meteo Meteorological API (Agro-weather service)
  - Pytest (Automated unit and integration test suite)
- **Frontend**:
  - React 18 + Vite (High performance bundle)
  - Lucide React (Agricultural icon set)
  - Recharts (Interactive price charts, feature importances, weather forecasts)
  - Canvas Confetti (Action plan celebration)
  - Custom Agriculture Design System (Emerald Green, Amber, Slate palette, glassmorphism cards)

---

## 📁 Clean Professional Project Structure

```
smartagri/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py               # Application settings & directory constants
│   │   ├── routers/
│   │   │   ├── crop_recommendation.py  # Crop advisor API
│   │   │   ├── yield_prediction.py     # Yield prediction API
│   │   │   ├── disease_detection.py    # Leaf vision diagnosis API
│   │   │   ├── weather_advisory.py     # Agro-weather API
│   │   │   ├── market_intelligence.py  # Mandi price trends API
│   │   │   ├── government_schemes.py   # Scheme discovery API
│   │   │   ├── farmer_profile.py       # Profile state & presets API
│   │   │   ├── ai_assistant.py         # Central AI chat orchestrator API
│   │   │   ├── action_plan.py          # Farm Action Plan generator API
│   │   │   └── models_info.py          # Benchmark metrics & dataset provenance API
│   │   ├── schemas/
│   │   │   └── __init__.py             # Pydantic validation schemas
│   │   ├── services/                   # Business logic & inference engines
│   │   └── main.py                     # FastAPI entry point & CORS
│   ├── data/
│   │   ├── raw/                        # 5 Raw Kaggle datasets
│   │   ├── processed/                  # Cleaned CSVs, JSON indices, remedies
│   │   └── samples/                    # Sample leaf images for instant testing
│   ├── models/                         # Exported ML model artifacts (.joblib, JSON)
│   ├── scripts/                        # Reproducible data ingestion & training scripts
│   ├── tests/                          # Pytest automated test suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/                 # Navbar, Sidebar, ActionPlanModal, DemoTourModal
│   │   ├── context/                    # FarmerProvider global state
│   │   ├── pages/                      # 11 complete module pages
│   │   ├── services/                   # API client service
│   │   ├── index.css                   # Agriculture design system
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## ⚡ Quick Start & Local Setup Instructions

### Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- Node.js v18+ & npm

### 1. Backend Setup & Model Training
```bash
cd backend

# 1. Create and activate virtual environment
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Ingest all 5 datasets and train ML models (Reproducible pipeline)
python scripts/download_and_process_data.py
python scripts/train_crop_recommendation.py
python scripts/train_yield_prediction.py
python scripts/setup_disease_model.py

# 4. Run automated test suite
pytest -v tests/

# 5. Start backend server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend API docs will be live at `http://127.0.0.1:8000/docs` and health check at `http://127.0.0.1:8000/health`.*

### 2. Frontend Setup & Launch
```bash
cd frontend

# Install frontend dependencies
npm install

# Start Vite development server
npm run dev -- --host 127.0.0.1 --port 5173
```
*Open your browser and navigate to `http://127.0.0.1:5173` to experience the complete platform!*

---

## 🧪 API Endpoints Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/crop-recommendation/predict` | `POST` | Predicts top crops matching NPK, pH, rainfall, and climate with feature importances |
| `/api/yield-prediction/predict` | `POST` | Regresses expected crop yield (Tons/Ha & Quintals/Acre) with driver breakdown |
| `/api/disease-detection/diagnose` | `POST` | Multi-part image upload for plant disease vision diagnosis |
| `/api/disease-detection/diagnose-sample` | `POST` | Diagnoses sample leaf images from gallery |
| `/api/disease-detection/samples` | `GET` | Lists available test leaf image gallery |
| `/api/weather/advisory` | `GET` | Fetches real-time weather, 7-day forecast, and agro-meteorological advisory |
| `/api/market/filters` | `GET` | Returns available state, district, mandi, and commodity filter options |
| `/api/market/trends` | `GET` | Retrieves historical mandi price trends, modal spread, and volatility index |
| `/api/market/where-to-sell` | `GET` | Ranks top mandis in the state by average price realization |
| `/api/schemes/search` | `GET` | Searches government schemes by keyword and category |
| `/api/schemes/match-profile` | `POST` | Ranks schemes customized to farmer profile landholding and tier |
| `/api/assistant/chat` | `POST` | Central tool-augmented conversational assistant |
| `/api/action-plan/generate` | `GET/POST`| Synthesizes the consolidated 8-point Farm Action Plan |
| `/api/models-info/summary` | `GET` | Exposes model evaluation metrics, dataset provenance, and confusion matrix |

---

## 🛡️ AI Safety, Ethics & Transparency

1. **Uncertainty Communication**: Predictions communicate uncertainty intervals and confidence scores. We never promise guaranteed profits, cures, or yields.
2. **Official Verification Links**: Every government scheme links directly to official portals (**MyScheme.gov.in**, PM-KISAN) and displays standard verification alerts.
3. **Historical Data Transparency**: Mandi wholesale price datasets are clearly attributed as historical reference records to prevent confusing historical trends with real-time auction bids.

---

## 📜 Dataset Attribution & Licensing

- **Crop Recommendation**: Arka Bhowmik, Kaggle (CC0: Public Domain)
- **PlantVillage Dataset**: Tushar Sharma / Hughes & Salathé, Penn State (CC BY-SA 4.0)
- **Crop Yield in India**: Aaron Gebremariam, Kaggle (Open Data Commons / CC0)
- **Daily Wholesale Commodity Prices India Mandis**: Ishan Kat, Kaggle / Agmarknet (GODL-India)
- **Indian Government Schemes**: Jainam Gada, Kaggle (Open Government Data)
