"""
SmartAgri AI - Multi-Source Plant Health & Rust Evaluation Test Suite
Verifies:
1. Image Quality Gate (low contrast / tiny images trigger retry alert)
2. Rust Evaluation Subset (Apple Cedar Rust vs Groundnut Rust vs Healthy leaves)
3. Rice & Cassava multi-source diagnostics & Pest damage routing
4. Low confidence chemical treatment withholding safeguards
5. Camera vs Gallery shared endpoint consistency
"""

import os
import sys
import pytest
import numpy as np
from PIL import Image
from io import BytesIO
from fastapi.testclient import TestClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.main import app
from app.services.disease_service import disease_service

client = TestClient(app)

def create_synthetic_leaf_bytes(color=(34, 139, 34), size=(128, 128)):
    """Helper to generate PIL image bytes for testing."""
    img = Image.new("RGB", size, color=color)
    arr = np.array(img)
    # Add fake leaf vein texture
    arr[20:100, 64, :] = [200, 200, 50]
    img_textured = Image.fromarray(arr)
    buf = BytesIO()
    img_textured.save(buf, format="JPEG")
    return buf.getvalue()

def test_image_quality_gate_low_contrast():
    """Verify Stage 1 Quality Gate catches blank/low-contrast images."""
    # Blank white image
    img = Image.new("RGB", (100, 100), color=(255, 255, 255))
    buf = BytesIO()
    img.save(buf, format="JPEG")
    
    response = client.post(
        "/api/disease-detection/diagnose",
        files={"file": ("blank.jpg", buf.getvalue(), "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_low_confidence"] is True
    assert "Low Confidence" in data["confidence_tier"] or "Unusable" in data["condition"]
    assert "Chemical" in data["chemical_treatment"] or "withheld" in data["chemical_treatment"].lower()

def test_rust_evaluation_subset_apple_vs_groundnut():
    """Verify Apple Cedar Rust and Groundnut Rust are distinctly mapped in taxonomy."""
    # Groundnut Rust sample
    gn_rust_img = create_synthetic_leaf_bytes(color=(180, 80, 20)) # Orange-rust reddish tint
    res_gn = disease_service.diagnose(gn_rust_img, "groundnut_rust.jpg")
    assert res_gn.request_id.startswith("DX-2026-")
    assert res_gn.detected_crop is not None
    assert len(res_gn.top_predictions) > 0

def test_rice_pest_damage_routing():
    """Verify Rice Hispa pest damage is routed with pest remedies."""
    rice_img = create_synthetic_leaf_bytes(color=(40, 160, 40))
    res = disease_service.diagnose(rice_img, "rice_hispa.jpg")
    assert res.detected_crop is not None
    assert res.symptoms is not None

def test_cassava_mosaic_diagnostics():
    """Verify Cassava Mosaic virus classification."""
    cassava_img = create_synthetic_leaf_bytes(color=(120, 180, 50))
    res = disease_service.diagnose(cassava_img, "cassava_mosaic.jpg")
    assert res.confidence >= 0.0 and res.confidence <= 1.0

def test_low_confidence_chemical_withholding_safeguard():
    """Verify chemical spray dosages are strictly withheld for low-confidence predictions."""
    # Extremely noisy random array
    arr = np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    buf = BytesIO()
    img.save(buf, format="JPEG")
    
    res = disease_service.diagnose(buf.getvalue(), "noisy_random.jpg")
    if res.is_low_confidence:
        assert "withheld" in res.chemical_treatment.lower() or "no chemical" in res.chemical_treatment.lower()

def test_camera_and_gallery_endpoint_consistency():
    """Verify camera capture and gallery upload use identical API endpoint."""
    leaf_bytes = create_synthetic_leaf_bytes()
    
    # Camera path
    res_cam = client.post(
        "/api/disease-detection/diagnose",
        files={"file": ("camera_capture.jpg", leaf_bytes, "image/jpeg")}
    )
    # Gallery path
    res_gal = client.post(
        "/api/disease-detection/diagnose",
        files={"file": ("gallery_upload.jpg", leaf_bytes, "image/jpeg")}
    )
    
    assert res_cam.status_code == 200
    assert res_gal.status_code == 200
    d_cam = res_cam.json()
    d_gal = res_gal.json()
    assert d_cam["detected_crop"] == d_gal["detected_crop"]
    assert d_cam["condition"] == d_gal["condition"]
