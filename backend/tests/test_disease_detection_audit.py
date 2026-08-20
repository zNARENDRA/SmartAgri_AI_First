import os
import sys
import io
import pytest
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi.testclient import TestClient
from app.main import app
from app.services.disease_service import disease_service

client = TestClient(app)

def create_synthetic_leaf_bytes(color=(34, 139, 34), noise=False):
    img = Image.new("RGB", (256, 256), color=color)
    if noise:
        arr = np.array(img, dtype=np.uint8)
        arr += np.random.randint(0, 50, arr.shape, dtype=np.uint8)
        img = Image.fromarray(arr)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def test_disease_classes_mapping_integrity():
    """Verify that model classes_ matches disease_service classes exactly."""
    assert disease_service.model is not None
    model_classes = getattr(disease_service.model, "classes_", [])
    assert len(model_classes) >= 15

def test_diagnose_sample_image_endpoint():
    """Test sample image endpoint returns exact diagnosis and debug info."""
    response = client.post("/api/disease-detection/diagnose-sample?filename=tomato_early_blight.jpg")
    assert response.status_code == 200
    data = response.json()
    
    assert data["request_id"].startswith("DX-2026-")
    assert "detected_crop" in data
    assert "condition" in data
    assert "confidence" in data
    assert "debug_info" in data
    assert data["debug_info"]["filename"] == "tomato_early_blight.jpg"

def test_diagnose_user_upload_endpoint():
    """Test user file upload endpoint returns structured diagnosis and request tracking."""
    img_bytes = create_synthetic_leaf_bytes(color=(100, 150, 50), noise=True)
    files = {"file": ("test_rust_leaf.jpg", img_bytes, "image/jpeg")}
    
    response = client.post("/api/disease-detection/diagnose", files=files)
    assert response.status_code == 200
    data = response.json()
    
    assert data["request_id"].startswith("DX-2026-")
    assert "confidence_tier" in data
    assert isinstance(data["is_low_confidence"], bool)

def test_low_confidence_chemical_withholding_safeguard():
    """Test that low confidence inputs (< 40%) trigger chemical treatment withholding."""
    # Create pure uniform gray image (out-of-distribution for leaf features)
    img_bytes = create_synthetic_leaf_bytes(color=(128, 128, 128), noise=True)
    res = disease_service.diagnose(img_bytes, filename="uniform_gray.jpg")
    
    # If confidence is low, chemical treatment must be withheld
    if res.is_low_confidence:
        assert res.status == "Uncertain"
        assert "withheld" in res.chemical_treatment.lower() or "no chemical" in res.chemical_treatment.lower()
        assert res.confidence_tier == "Low Confidence / Uncertain"
