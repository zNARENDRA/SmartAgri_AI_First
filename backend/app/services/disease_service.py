import os
import json
import uuid
import joblib
import numpy as np
from PIL import Image
from io import BytesIO
from app.core.config import MODELS_DIR, DATA_PROCESSED, SQLITE_DB_PATH
from app.db import query_as_dicts
from app.schemas import DiseaseDiagnosisResponse

def extract_image_features(image_bytes_or_pil):
    if isinstance(image_bytes_or_pil, bytes):
        img = Image.open(BytesIO(image_bytes_or_pil)).convert("RGB")
    elif isinstance(image_bytes_or_pil, Image.Image):
        img = image_bytes_or_pil.convert("RGB")
    else:
        img = Image.open(image_bytes_or_pil).convert("RGB")
        
    img_resized = img.resize((128, 128))
    arr = np.array(img_resized, dtype=np.float32) / 255.0
    
    means = arr.mean(axis=(0, 1))
    stds = arr.std(axis=(0, 1))
    
    r_hist, _ = np.histogram(arr[:, :, 0], bins=16, range=(0, 1), density=True)
    g_hist, _ = np.histogram(arr[:, :, 1], bins=16, range=(0, 1), density=True)
    b_hist, _ = np.histogram(arr[:, :, 2], bins=16, range=(0, 1), density=True)
    
    grid_features = []
    h_step, w_step = 32, 32
    for r in range(4):
        for c in range(4):
            sub = arr[r*h_step:(r+1)*h_step, c*w_step:(c+1)*w_step, :]
            grid_features.extend(sub.mean(axis=(0, 1)))
            grid_features.extend(sub.std(axis=(0, 1)))
            
    exg = 2 * arr[:, :, 1] - arr[:, :, 0] - arr[:, :, 2]
    exg_mean = float(exg.mean())
    exg_std = float(exg.std())
    
    features = np.concatenate([
        means, stds, r_hist, g_hist, b_hist, np.array(grid_features), np.array([exg_mean, exg_std])
    ])
    return features

from fastapi import HTTPException

class DiseaseDetectionService:
    def __init__(self):
        model_file = os.path.join(MODELS_DIR, "plant_disease_model.joblib")
        if os.path.exists(model_file):
            self.artifact = joblib.load(model_file)
            self.model = self.artifact["model"]
            self.classes = self.artifact["classes"]
        else:
            self.model = None
            self.classes = []
            
        self.remedies = {}
        self.pest_remedies = {}
        if os.path.exists(SQLITE_DB_PATH):
            try:
                db_rows = query_as_dicts("SELECT * FROM disease_remedies")
                for row in db_rows:
                    cls_id = row.get("class_id")
                    if cls_id:
                        self.remedies[cls_id] = {
                            "crop": row.get("crop"),
                            "condition": row.get("condition"),
                            "status": row.get("status"),
                            "severity": row.get("severity"),
                            "pathogen": row.get("pathogen"),
                            "symptoms": row.get("symptoms"),
                            "immediate_action": row.get("immediate_action"),
                            "organic_treatment": row.get("organic_treatment"),
                            "chemical_treatment": row.get("chemical_treatment"),
                            "prevention": row.get("prevention")
                        }
                
                pest_rows = query_as_dicts("SELECT * FROM pest_remedies")
                for row in pest_rows:
                    p_id = row.get("pest_id")
                    if p_id:
                        self.pest_remedies[p_id] = {
                            "crop": row.get("crop"),
                            "pest_name": row.get("pest_name"),
                            "damage_pattern": row.get("damage_pattern"),
                            "organic_control": row.get("organic_control"),
                            "chemical_control": row.get("chemical_control"),
                            "prevention": row.get("prevention")
                        }
            except Exception as e:
                print(f"[!] Exception loading disease & pest remedies from SQLite DB: {e}")
                self.remedies = {}
                self.pest_remedies = {}
        elif os.path.exists(os.path.join(DATA_PROCESSED, "disease_remedies.json")):
            remedies_file = os.path.join(DATA_PROCESSED, "disease_remedies.json")
            with open(remedies_file, "r", encoding="utf-8") as f:
                self.remedies = json.load(f)

    def diagnose(self, image_data, filename: str = "uploaded_leaf.jpg") -> DiseaseDiagnosisResponse:
        if self.model is None:
            raise HTTPException(status_code=503, detail="Plant disease vision model is not loaded or uninitialized.")
            
        request_id = f"DX-2026-{uuid.uuid4().hex[:6].upper()}"
        
        # Extract features
        feat = extract_image_features(image_data)
        X = np.array([feat])
        
        # Use exact classifier classes_ list to prevent index misalignment
        model_classes = getattr(self.model, "classes_", self.classes)
        if not isinstance(model_classes, list):
            model_classes = list(model_classes)
            
        probs = self.model.predict_proba(X)[0]
        top_indices = np.argsort(probs)[::-1][:3]
        
        top_predictions = []
        for idx in top_indices:
            cls_name = model_classes[idx]
            conf = float(probs[idx])
            rem_info = self.remedies.get(cls_name, {})
            top_predictions.append({
                "class_id": cls_name,
                "crop": rem_info.get("crop", cls_name.split("___")[0]),
                "condition": rem_info.get("condition", cls_name.split("___")[-1].replace("_", " ")),
                "status": rem_info.get("status", "Healthy" if "healthy" in cls_name.lower() else "Diseased"),
                "confidence": round(conf, 4),
                "confidence_percentage": f"{conf * 100:.1f}%"
            })
            
        best_cls = model_classes[top_indices[0]]
        best_conf = float(probs[top_indices[0]])
        rem = self.remedies.get(best_cls, {})
        
        # Determine confidence threshold tier
        # Thresholds: High >= 0.60, Moderate >= 0.40 & < 0.60, Low < 0.40
        if best_conf >= 0.60:
            confidence_tier = "High Confidence"
            is_low_confidence = False
        elif best_conf >= 0.40:
            confidence_tier = "Moderate Confidence"
            is_low_confidence = False
        else:
            confidence_tier = "Low Confidence / Uncertain"
            is_low_confidence = True

        if is_low_confidence:
            crop_name = rem.get("crop", best_cls.split("___")[0])
            condition_name = f"Uncertain Condition (Low Model Confidence: {best_conf * 100:.1f}%)"
            status = "Uncertain"
            severity = "Uncertain"
            pathogen = "Unconfirmed (Low Model Confidence)"
            symptoms = f"The model could not identify distinctive leaf disease patterns with high confidence (Top match: {best_cls.replace('___', ' - ')} at {best_conf * 100:.1f}% confidence)."
            immediate_actions = "Please retake a closer, well-lit photograph of the affected leaf against a plain background, or consult a local Krishi Vigyan Kendra (KVK) extension officer."
            organic_treatment = "Specific bio-treatment recommendations are withheld due to low diagnosis confidence. Retake photo with clear leaf detail."
            chemical_treatment = "Chemical treatment and fungicide spray dosages are strictly withheld for uncertain predictions to prevent potential crop damage or improper pesticide usage."
            prevention_measures = "Maintain optimal crop spacing, adequate sunlight, and balanced fertigation while monitoring leaf health for clear symptoms."
        else:
            crop_name = rem.get("crop", best_cls.split("___")[0])
            condition_name = rem.get("condition", best_cls.split("___")[-1].replace("_", " "))
            status = rem.get("status", "Healthy" if "healthy" in best_cls.lower() else "Diseased")
            severity = rem.get("severity", "None" if status == "Healthy" else "Moderate")
            pathogen = rem.get("pathogen", "N/A (Healthy Crop)")
            symptoms = rem.get("symptoms", "Healthy leaf structure with uniform pigmentation.")
            immediate_actions = rem.get("immediate_action", "Maintain regular field hygiene and standard nutrition.")
            organic_treatment = rem.get("organic_treatment", "Apply bio-fertilizer or vermicompost tea.")
            chemical_treatment = rem.get("chemical_treatment", "No chemical intervention needed.")
            prevention_measures = rem.get("prevention", "Maintain optimal crop spacing and drip irrigation.")

        debug_info = {
            "request_id": request_id,
            "filename": filename,
            "image_size_bytes": len(image_data) if isinstance(image_data, bytes) else "N/A (File path)",
            "extracted_features_dim": len(feat),
            "total_model_classes": len(model_classes),
            "confidence_tier": confidence_tier,
            "is_out_of_distribution": is_low_confidence,
            "top_3_predictions": top_predictions
        }

        return DiseaseDiagnosisResponse(
            request_id=request_id,
            is_low_confidence=is_low_confidence,
            confidence_tier=confidence_tier,
            detected_crop=crop_name,
            condition=condition_name,
            status=status,
            severity=severity,
            confidence=round(best_conf, 4),
            confidence_percentage=f"{best_conf * 100:.1f}%",
            pathogen=pathogen,
            symptoms=symptoms,
            immediate_actions=immediate_actions,
            organic_treatment=organic_treatment,
            chemical_treatment=chemical_treatment,
            prevention_measures=prevention_measures,
            top_predictions=top_predictions,
            disclaimer="AI-assisted image diagnosis. Symptoms should be verified by a plant pathologist or local Krishi Vigyan Kendra (KVK) expert before applying regulated chemical fungicides.",
            debug_info=debug_info
        )

disease_service = DiseaseDetectionService()
