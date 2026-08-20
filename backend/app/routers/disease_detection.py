import os
import json
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from app.schemas import DiseaseDiagnosisResponse
from app.services.disease_service import disease_service
from app.core.config import DATA_SAMPLES, MODELS_DIR

router = APIRouter(prefix="/disease-detection", tags=["Plant Disease Detection"])

@router.post("/diagnose", response_model=DiseaseDiagnosisResponse)
async def diagnose_leaf_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JPG, JPEG, or PNG image.")
    
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size exceeds 10MB limit.")
        
    try:
        return disease_service.diagnose(contents, filename=file.filename or "uploaded_leaf.jpg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Leaf diagnosis inference failed: {str(e)}")

@router.post("/diagnose-sample", response_model=DiseaseDiagnosisResponse)
def diagnose_sample_image(filename: str = Query(..., description="Sample filename from the gallery")):
    sample_path = os.path.join(DATA_SAMPLES, filename)
    if not os.path.exists(sample_path):
        raise HTTPException(status_code=404, detail="Sample image not found.")
        
    try:
        return disease_service.diagnose(sample_path, filename=filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sample diagnosis failed: {str(e)}")

@router.get("/samples")
def list_sample_images():
    if not os.path.exists(DATA_SAMPLES):
        return []
    samples = []
    for f in sorted(os.listdir(DATA_SAMPLES)):
        if f.endswith((".jpg", ".png", ".jpeg")):
            # Friendly label
            clean_name = f.replace(".jpg", "").replace(".png", "").replace("_", " ").title()
            samples.append({
                "filename": f,
                "label": clean_name,
                "url": f"/static/samples/{f}"
            })
    return samples

@router.get("/classes")
def get_classes():
    return {
        "total_classes": len(disease_service.classes),
        "classes": disease_service.classes,
        "remedies": disease_service.remedies
    }

@router.get("/metrics")
def get_metrics():
    metrics_path = os.path.join(MODELS_DIR, "plant_disease_metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"message": "Metrics not found"}
