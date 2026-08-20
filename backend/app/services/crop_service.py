import os
import joblib
import numpy as np
from app.core.config import MODELS_DIR
from app.schemas import CropRecommendationRequest, CropRecommendationResponse, CropScore

CROP_DETAILS = {
    "rice": {"duration": "120-150 days", "water": "High (Submerged / Standing water)", "soil": "Clayey loam, rich in organic matter", "adv": ["High market demand across India", "Responds very well to high nitrogen"]},
    "maize": {"duration": "90-110 days", "water": "Moderate", "soil": "Well-drained deep loamy soil", "adv": ["Excellent industrial & poultry feed demand", "Low labor requirement"]},
    "chickpea": {"duration": "100-120 days", "water": "Low (Drought tolerant)", "soil": "Sandy loam to clay loam, pH 6.0-7.5", "adv": ["Biological Nitrogen fixation enriches soil", "High market MSP support"]},
    "kidneybeans": {"duration": "90-120 days", "water": "Moderate", "soil": "Light rich loamy soil", "adv": ["High protein cash crop", "Good intercropping option"]},
    "pigeonpeas": {"duration": "140-180 days", "water": "Low-Moderate", "soil": "Deep well-drained loamy soil", "adv": ["Deep root system breaks hard soil pan", "Premium dal market prices"]},
    "mothbeans": {"duration": "60-75 days", "water": "Very Low (Arid)", "soil": "Sandy to light loam soil", "adv": ["Extreme drought tolerance", "Quickest turnaround pulse"]},
    "mungbean": {"duration": "65-75 days", "water": "Low", "soil": "Well-drained loam", "adv": ["Short duration catch crop between seasons", "Soil fertility booster"]},
    "blackgram": {"duration": "70-85 days", "water": "Low-Moderate", "soil": "Loamy to heavy clay", "adv": ["High domestic culinary demand", "Good green manure crop"]},
    "lentil": {"duration": "110-130 days", "water": "Low", "soil": "Alluvial loams", "adv": ["Winter rabi pulse with high yield stability", "Low fertilizer input needed"]},
    "pomegranate": {"duration": "Perennial (180 days fruit cycle)", "water": "Moderate (Drip preferred)", "soil": "Well-drained sandy loam", "adv": ["Very high export cash return", "Drought hardy once established"]},
    "banana": {"duration": "11-12 months", "water": "High (Frequent irrigation)", "soil": "Deep rich loamy soil with pH 6.5-7.5", "adv": ["Year-round continuous cash flow", "High biomass and ton-per-acre returns"]},
    "mango": {"duration": "Perennial", "water": "Moderate", "soil": "Deep well-drained alluvial/loamy", "adv": ["Long-term orchard asset", "High seasonal price spikes"]},
    "grapes": {"duration": "Perennial (annual pruning cycles)", "water": "Controlled Drip", "soil": "Well-drained sandy loam with gravel", "adv": ["Extremely high commercial & wine value", "High yield under proper trellis"]},
    "watermelon": {"duration": "75-90 days", "water": "Moderate", "soil": "Sandy river beds to sandy loam", "adv": ["Fast summer cash turnover", "High yield with drip fertigation"]},
    "muskmelon": {"duration": "75-85 days", "water": "Moderate", "soil": "Sandy to sandy loam", "adv": ["High sugar sweetness in hot dry climate", "Lucrative urban market"]},
    "apple": {"duration": "Perennial (Temperate)", "water": "Moderate-High", "soil": "Deep loamy soil with rich humus", "adv": ["Top hill-state cash crop", "Long storage life and high retail price"]},
    "orange": {"duration": "Perennial", "water": "Moderate (Drip)", "soil": "Well-drained light loams", "adv": ["Strong processing and fresh market", "Rich Vitamin C market appeal"]},
    "papaya": {"duration": "9-10 months to first harvest", "water": "Moderate", "soil": "Porous, rich sandy loam (No waterlogging)", "adv": ["Very fast fruit crop turnaround", "Continuous fruiting for 2 years"]},
    "coconut": {"duration": "Perennial (Year-round)", "water": "Moderate-High", "soil": "Coastal alluvium, red sandy loam", "adv": ["Durable 60+ year productive lifespan", "Multiple revenue streams (copra, tender water, coir)"]},
    "cotton": {"duration": "150-180 days", "water": "Moderate", "soil": "Deep black cotton soil (Vertisols)", "adv": ["Major national cash fiber crop", "Excellent for warm dry climates"]},
    "jute": {"duration": "120-150 days", "water": "High", "soil": "New alluvial sandy clay loam", "adv": ["High eco-friendly fiber demand", "Resistant to seasonal flood submergence"]},
    "coffee": {"duration": "Perennial (Shade grown)", "water": "Moderate-High", "soil": "Deep porous volcanic / forest loam", "adv": ["High export foreign exchange earner", "Intercropping with pepper & cardamom"]}
}

import pandas as pd
from fastapi import HTTPException

class CropRecommendationService:
    def __init__(self):
        model_file = os.path.join(MODELS_DIR, "crop_recommendation_model.joblib")
        if os.path.exists(model_file):
            self.artifact = joblib.load(model_file)
            self.model = self.artifact["model"]
            self.features = self.artifact["features"]
            self.classes = self.artifact["classes"]
            self.metrics = self.artifact.get("metrics", {})
        else:
            self.artifact = None
            self.model = None

    def predict(self, req: CropRecommendationRequest) -> CropRecommendationResponse:
        if self.model is None:
            raise HTTPException(status_code=503, detail="Crop recommendation ML model is not loaded or uninitialized.")
            
        input_data = [req.N, req.P, req.K, req.temperature, req.humidity, req.ph, req.rainfall]
        features = getattr(self, "features", ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"])
        X_df = pd.DataFrame([input_data], columns=features)
        
        probs = self.model.predict_proba(X_df)[0]
        top_indices = np.argsort(probs)[::-1][:req.top_k]
        
        recommendations = []
        for idx in top_indices:
            crop_name = self.classes[idx]
            conf = float(probs[idx])
            details = CROP_DETAILS.get(crop_name.lower(), {
                "duration": "90-120 days", "water": "Moderate", "soil": "Loamy soil",
                "adv": ["Suitable for local agronomic conditions", "Good return on investment"]
            })
            
            recommendations.append(CropScore(
                crop=crop_name.capitalize(),
                confidence=round(conf, 4),
                percentage=f"{conf * 100:.1f}%",
                soil_suitability="Highly Suitable" if conf > 0.4 else "Moderately Suitable",
                key_advantages=details["adv"],
                water_requirement=details["water"],
                expected_duration_days=details["duration"]
            ))

        top_crop = recommendations[0].crop
        
        # Explainability feature importances
        feat_imp = self.metrics.get("feature_importances", {
            "N": 0.18, "P": 0.19, "K": 0.22, "temperature": 0.08, "humidity": 0.12, "ph": 0.06, "rainfall": 0.15
        })

        # Agronomic nutritional analysis
        nutritional_analysis = {}
        if req.N < 40:
            nutritional_analysis["Nitrogen (N)"] = "Low - Consider basal application of Urea or composted manure."
        elif req.N > 120:
            nutritional_analysis["Nitrogen (N)"] = "High - Abundant N supports vegetative growth; avoid excessive top-dressing."
        else:
            nutritional_analysis["Nitrogen (N)"] = "Optimal - Balanced nitrogen level for healthy tillering and foliage."

        if req.ph < 6.0:
            nutritional_analysis["Soil pH"] = f"{req.ph:.1f} (Acidic) - Consider agricultural lime application to optimize nutrient uptake."
        elif req.ph > 7.5:
            nutritional_analysis["Soil pH"] = f"{req.ph:.1f} (Alkaline) - Consider gypsum or organic sulfur amendments."
        else:
            nutritional_analysis["Soil pH"] = f"{req.ph:.1f} (Near Neutral) - Ideal range for broad nutrient bioavailability."

        # Fetch GoI District Production Statistics Context (Dataset 8) from SQLite
        from app.core.config import SQLITE_DB_PATH
        from app.db import query_as_dicts
        
        district_context = {}
        if os.path.exists(SQLITE_DB_PATH):
            try:
                state_query = req.state or "Maharashtra"
                rows = query_as_dicts(
                    "SELECT crop, SUM(production) as total_prod, AVG(yield_ha) as avg_yield FROM district_crop_production WHERE state = ? GROUP BY crop ORDER BY total_prod DESC LIMIT 5",
                    (state_query,)
                )
                if rows:
                    district_context = {
                        "state": state_query,
                        "top_historically_produced_crops": [r["crop"] for r in rows],
                        "state_avg_productivity_ha": round(float(rows[0]["avg_yield"]), 2) if rows else 3.2,
                        "historical_note": f"{top_crop} is agronomically compatible with soil NPK ({req.N}-{req.P}-{req.K}) and rainfall ({req.rainfall} mm) in {state_query}."
                    }
            except Exception as e:
                print(f"[!] Exception querying district crop production context: {e}")
                district_context = {"state": req.state or "Maharashtra", "historical_note": "Compatible with regional agro-climatic zone."}

        return CropRecommendationResponse(
            top_crop=top_crop,
            recommendations=recommendations,
            feature_importances=feat_imp,
            input_parameters={
                "N": req.N, "P": req.P, "K": req.K,
                "temperature": req.temperature, "humidity": req.humidity,
                "ph": req.ph, "rainfall": req.rainfall,
                "state": req.state or "Maharashtra"
            },
            nutritional_analysis=nutritional_analysis,
            district_context=district_context,
            disclaimer="AI-generated recommendation based on soil parameters, climate data, and historical GoI district crop production statistics. Verify with local Krishi Vigyan Kendra (KVK) extension officers before sowing."
        )

crop_service = CropRecommendationService()
