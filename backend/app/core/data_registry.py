"""
KrishiKalyan AI - Data Source & AI Registry
Central repository of provenance, provider metadata, URLs, licenses, and module usage across all 11 datasets.
"""

DATA_REGISTRY = [
    {
        "id": "ds-1",
        "name": "Crop Recommendation Dataset",
        "category": "Soil & Climate",
        "provider": "Kaggle (arkabhowmik)",
        "url": "https://www.kaggle.com/datasets/arkabhowmik/crop-recommendation",
        "records": 2200,
        "license": "CC0: Public Domain",
        "attribution": "Soil NPK, pH, temperature, humidity, and rainfall matching across 22 crops.",
        "module_used": "AI Crop Advisor & Recommendation Engine"
    },
    {
        "id": "ds-2",
        "name": "PlantVillage Leaf Disease Dataset",
        "category": "Computer Vision & Diagnostics",
        "provider": "PlantVillage / Kaggle (tushar5harma)",
        "url": "https://www.kaggle.com/datasets/tushar5harma/plant-village-dataset-updated",
        "records": 27000,
        "classes": 27,
        "license": "CC BY-SA 4.0",
        "attribution": "High-resolution leaf pathology images across Tomato, Potato, Corn, Apple, Grape, Pepper.",
        "module_used": "Plant Disease Diagnosis & Camera Scanner"
    },
    {
        "id": "ds-3",
        "name": "Crop Yield Statistics Dataset",
        "category": "Agricultural Economics & Yield",
        "provider": "Kaggle (aarongebremariam)",
        "url": "https://www.kaggle.com/datasets/aarongebremariam/crop-yield",
        "records": 8550,
        "license": "Open Data",
        "attribution": "State-season crop production statistics, fertilizer dosage, pesticide usage, and acreage.",
        "module_used": "Crop Yield Prediction Engine"
    },
    {
        "id": "ds-4",
        "name": "Daily Wholesale Mandi Commodity Prices",
        "category": "Market Intelligence",
        "provider": "Agmarknet / Kaggle (ishankat)",
        "url": "https://www.kaggle.com/datasets/ishankat/daily-wholesale-commodity-prices-india-mandis",
        "records": 57330,
        "license": "Open Government Data (OGD) License India",
        "attribution": "Daily APMC mandi modal, min, max commodity price arrivals across 600+ Indian mandis.",
        "module_used": "Market Intelligence & Smart Ranker"
    },
    {
        "id": "ds-5",
        "name": "Indian Government Farmer Schemes",
        "category": "Government Schemes & Subsidies",
        "provider": "MyScheme.gov.in / Kaggle (jainamgada45)",
        "url": "https://www.kaggle.com/datasets/jainamgada45/indian-government-schemes",
        "records": 10,
        "license": "Public Information",
        "attribution": "Central & State agricultural subsidies, eligibility criteria, benefits, and application steps.",
        "module_used": "Government Subsidy Discovery Engine"
    },
    {
        "id": "ds-6",
        "name": "Indian Historical Crop Yield & Weather Data",
        "category": "Climate & Crop Productivity",
        "provider": "Kaggle (zoya77)",
        "url": "https://www.kaggle.com/datasets/zoya77/indian-historical-crop-yield-and-weather-data",
        "records": 1512,
        "license": "Open Data",
        "attribution": "Historical weather parameters (temperature, solar radiation, wind speed) matched with crop yields.",
        "module_used": "Enhanced Yield Engine & Climate Risk Analytics"
    },
    {
        "id": "ds-7",
        "name": "Crop Yield Data with Soil and Weather",
        "category": "Agronomic Soil & Climate",
        "provider": "Kaggle (anshumish)",
        "url": "https://www.kaggle.com/datasets/anshumish/crop-yield-data-with-soil-and-weather-dataset",
        "records": 4200,
        "license": "CC0: Public Domain",
        "attribution": "Integrated Soil NPK, pH, weather variables, and crop yield productivity indices.",
        "module_used": "Soil-Climate Compatibility Engine & Crop Advisor"
    },
    {
        "id": "ds-8",
        "name": "GoI District-wise Season-wise Crop Production Statistics",
        "category": "District Agricultural Statistics",
        "provider": "Ministry of Agriculture / Data.gov.in",
        "url": "https://www.data.gov.in/catalog/district-wise-season-wise-crop-production-statistics-0",
        "records": 1665,
        "license": "Open Government Data (OGD) License India",
        "attribution": "Official GoI district-wise crop cultivated area, annual production, and yield productivity benchmarks.",
        "module_used": "District Agricultural Intelligence & Crop Advisor"
    },
    {
        "id": "ds-9",
        "name": "GoI IMD Meteorological Rainfall Baseline & Anomalies",
        "category": "Historical Rainfall Intelligence",
        "provider": "India Meteorological Department (IMD) / Data.gov.in",
        "url": "https://data.gov.in/catalog/rainfall-india",
        "records": 168,
        "license": "Open Government Data (OGD) License India",
        "attribution": "Subdivision-wise monthly rainfall baselines, normal mm, actual mm, and monsoon departure percentage.",
        "module_used": "Rainfall Intelligence & Weather Advisory Engine"
    },
    {
        "id": "ds-10",
        "name": "Crop Disease + Insect Pest Detection (Agrithon)",
        "category": "Pest & Insect Diagnostics",
        "provider": "Agrithon / Kaggle (mohammedarfathr)",
        "url": "https://www.kaggle.com/datasets/mohammedarfathr/agrithon-round-1",
        "records": 5,
        "license": "CC BY 4.0",
        "attribution": "Crop pest/insect damage patterns, symptom questionnaires, and organic/chemical control protocols.",
        "module_used": "Multi-Stage Vision Disease & Pest Scanner"
    },
    {
        "id": "ds-11",
        "name": "ICAR Weather-Based Crop Advisories Knowledge Base",
        "category": "Agricultural RAG Knowledge Layer",
        "provider": "Indian Council of Agricultural Research (ICAR)",
        "url": "https://www.icar.org.in/weather-based-crop-advisory",
        "records": 30,
        "license": "Official Agricultural Guidance",
        "attribution": "Weather-triggered agronomic advisories by ICAR-CRRI, ICAR-CICR, ICAR-IIWBR, ICAR-IIPR, and CRIDA.",
        "module_used": "AI Farmer Assistant RAG Layer & Farm Action Plan"
    }
]

def get_registry_summary():
    return {
        "total_datasets": len(DATA_REGISTRY),
        "total_records": sum(ds.get("records", 0) for ds in DATA_REGISTRY),
        "sources": DATA_REGISTRY
    }
