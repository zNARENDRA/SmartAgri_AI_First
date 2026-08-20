import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure backend root is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.main import app
from app.core.config import SQLITE_DB_PATH
from app.db import query_as_dicts
from app.services.assistant_service import assistant_service
from app.schemas import AssistantQueryRequest, FarmerProfile

client = TestClient(app)

def test_data_registry_endpoint():
    """Verify GET /api/models-info/registry returns all data sources (at least 11, up to 17)."""
    response = client.get("/api/models-info/registry")
    assert response.status_code == 200
    data = response.json()
    assert "total_datasets" in data
    assert data["total_datasets"] >= 11
    assert len(data["sources"]) >= 11
    
    # Check data source IDs ds-1 through ds-11
    ds_ids = [ds["id"] for ds in data["sources"]]
    for i in range(1, 12):
        assert f"ds-{i}" in ds_ids

def test_sqlite_tables_existence():
    """Verify SQLite database contains all 12 tables for the 11 datasets."""
    assert os.path.exists(SQLITE_DB_PATH)
    tables = query_as_dicts("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [t["name"] for t in tables]
    
    expected_tables = [
        "crop_recommendations", "crop_yields", "mandi_prices", "mandi_analytics",
        "government_schemes", "disease_remedies", "historical_yield_weather",
        "crop_yield_soil_weather", "district_crop_production", "imd_rainfall",
        "pest_remedies", "icar_advisories", "raw_csv_files"
    ]
    for table in expected_tables:
        assert table in table_names

def test_raw_csv_files_storage():
    """Verify raw CSV files are stored with non-empty content in SQLite."""
    rows = query_as_dicts("SELECT filename, dataset_name, record_count FROM raw_csv_files")
    assert len(rows) > 0
    filenames = [r["filename"] for r in rows]
    assert "crop_recommendation_cleaned.csv" in filenames
    assert "mandi_prices_cleaned.csv" in filenames

def test_historical_yield_weather_records():
    """Verify Dataset 6 records exist in SQLite."""
    rows = query_as_dicts("SELECT COUNT(*) as cnt FROM historical_yield_weather")
    assert rows[0]["cnt"] > 0

def test_crop_yield_soil_weather_records():
    """Verify Dataset 7 records exist in SQLite."""
    rows = query_as_dicts("SELECT COUNT(*) as cnt FROM crop_yield_soil_weather")
    assert rows[0]["cnt"] > 0

def test_district_crop_production_records():
    """Verify Dataset 8 records exist in SQLite."""
    rows = query_as_dicts("SELECT COUNT(*) as cnt FROM district_crop_production")
    assert rows[0]["cnt"] > 0

def test_imd_rainfall_records():
    """Verify Dataset 9 records exist in SQLite."""
    rows = query_as_dicts("SELECT COUNT(*) as cnt FROM imd_rainfall")
    assert rows[0]["cnt"] > 0

def test_pest_remedies_records():
    """Verify Dataset 10 records exist in SQLite."""
    rows = query_as_dicts("SELECT COUNT(*) as cnt FROM pest_remedies")
    assert rows[0]["cnt"] > 0

def test_icar_advisories_records():
    """Verify Dataset 11 records exist in SQLite."""
    rows = query_as_dicts("SELECT COUNT(*) as cnt FROM icar_advisories")
    assert rows[0]["cnt"] > 0

def test_weather_advisory_imd_baseline_integration():
    """Verify GET /api/weather/advisory includes IMD rainfall baseline."""
    response = client.get("/api/weather/advisory?location=Pune&crop=Soybean")
    assert response.status_code == 200
    data = response.json()
    assert "imd_rainfall_baseline" in data
    assert data["imd_rainfall_baseline"] is not None
    assert "monsoon_status" in data["imd_rainfall_baseline"]

def test_realtime_weather_api():
    """Verify GET /api/weather/current returns real-time temperature and weather metrics."""
    response = client.get("/api/weather/current?location=Pune")
    assert response.status_code == 200
    data = response.json()
    assert "temperature_celsius" in data
    assert "humidity_percentage" in data
    assert "condition_text" in data
    assert data["temperature_celsius"] > -50 and data["temperature_celsius"] < 60

def test_geocoding_api():
    """Verify GET /api/weather/geocoding resolves location names to lat/lon."""
    response = client.get("/api/weather/geocoding?query=Ludhiana")
    assert response.status_code == 200
    data = response.json()
    assert "latitude" in data
    assert "longitude" in data

def test_yield_prediction_evaluation_and_climate_risk():
    """Verify POST /api/yield-prediction/predict includes model evaluation and climate risk index."""
    payload = {
        "crop": "Wheat",
        "state": "Punjab",
        "season": "Rabi",
        "area": 2.5,
        "annual_rainfall": 1050.0,
        "fertilizer": 110.0,
        "pesticide": 1.5
    }
    response = client.post("/api/yield-prediction/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "model_evaluation" in data
    assert "climate_risk_index" in data
    assert data["model_evaluation"]["r2_score"] > 0.9

def test_crop_recommendation_district_context():
    """Verify POST /api/crop-recommendation/predict includes district production context."""
    payload = {
        "N": 90, "P": 42, "K": 43,
        "temperature": 25.0, "humidity": 80.0, "ph": 6.5, "rainfall": 200.0,
        "top_k": 3, "state": "Maharashtra"
    }
    response = client.post("/api/crop-recommendation/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "district_context" in data
    assert data["district_context"]["state"] == "Maharashtra"

def test_ai_assistant_icar_rag():
    """Verify AI Assistant retrieves ICAR advisories for weather intent."""
    req = AssistantQueryRequest(
        message="What is the weather and crop advisory for Rice in monsoon?",
        farmer_profile=FarmerProfile(state="Punjab", current_crop="Rice")
    )
    res = assistant_service.process_query(req)
    assert "IMD Rainfall Intelligence" in res.tools_used[1] or "ICAR Weather-Based Crop Advisory RAG Layer" in res.tools_used[2]
    assert "Weather & Agro-Advisory" in res.detected_intent
