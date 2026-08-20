from typing import Dict, Any, List
from fastapi import APIRouter
from app.schemas import FarmerProfile

router = APIRouter(prefix="/profile", tags=["Farmer Profile"])

# In-memory active profile with persistent presets
ACTIVE_PROFILE = FarmerProfile(
    name="Ramesh Patil",
    state="Maharashtra",
    district="Nashik",
    village="Niphad",
    land_size_acres=3.5,
    soil_type="Black Soil (Regur)",
    soil_ph=6.8,
    nitrogen=75.0,
    phosphorus=45.0,
    potassium=40.0,
    current_crop="Soybean",
    farming_season="Kharif",
    irrigation_source="Drip Irrigation & Tube Well",
    farmer_category="Small (1-2 ha)"
)

PRESETS: List[Dict[str, Any]] = [
    {
        "preset_id": "mh_small_farmer",
        "label": "Ramesh Patil - Small Farmer (Nashik, Maharashtra)",
        "profile": {
            "name": "Ramesh Patil",
            "state": "Maharashtra",
            "district": "Nashik",
            "village": "Niphad",
            "land_size_acres": 3.5,
            "soil_type": "Black Soil (Regur)",
            "soil_ph": 6.8,
            "nitrogen": 75.0,
            "phosphorus": 45.0,
            "potassium": 40.0,
            "current_crop": "Soybean",
            "farming_season": "Kharif",
            "irrigation_source": "Drip Irrigation & Tube Well",
            "farmer_category": "Small (1-2 ha)"
        }
    },
    {
        "preset_id": "pb_medium_farmer",
        "label": "Sukhwinder Singh - Medium Farmer (Ludhiana, Punjab)",
        "profile": {
            "name": "Sukhwinder Singh",
            "state": "Punjab",
            "district": "Ludhiana",
            "village": "Khanna Kalan",
            "land_size_acres": 8.0,
            "soil_type": "Alluvial Loam",
            "soil_ph": 7.2,
            "nitrogen": 95.0,
            "phosphorus": 55.0,
            "potassium": 45.0,
            "current_crop": "Wheat",
            "farming_season": "Rabi",
            "irrigation_source": "Canal & Submersible Borewell",
            "farmer_category": "Medium (2-10 ha)"
        }
    },
    {
        "preset_id": "ka_horticulture_farmer",
        "label": "Ananya Gowda - Horticulture Grower (Mysuru, Karnataka)",
        "profile": {
            "name": "Ananya Gowda",
            "state": "Karnataka",
            "district": "Mysuru",
            "village": "Nanjangud",
            "land_size_acres": 2.0,
            "soil_type": "Red Sandy Loam",
            "soil_ph": 6.4,
            "nitrogen": 60.0,
            "phosphorus": 70.0,
            "potassium": 50.0,
            "current_crop": "Tomato",
            "farming_season": "Kharif",
            "irrigation_source": "Micro Drip Automation",
            "farmer_category": "Marginal (< 1 ha)"
        }
    }
]

@router.get("", response_model=FarmerProfile)
def get_current_profile():
    return ACTIVE_PROFILE

@router.post("", response_model=FarmerProfile)
def update_profile(profile: FarmerProfile):
    global ACTIVE_PROFILE
    ACTIVE_PROFILE = profile
    return ACTIVE_PROFILE

@router.get("/presets")
def get_profile_presets():
    return PRESETS

@router.post("/presets/{preset_id}", response_model=FarmerProfile)
def load_preset(preset_id: str):
    global ACTIVE_PROFILE
    for p in PRESETS:
        if p["preset_id"] == preset_id:
            ACTIVE_PROFILE = FarmerProfile(**p["profile"])
            return ACTIVE_PROFILE
    return ACTIVE_PROFILE
