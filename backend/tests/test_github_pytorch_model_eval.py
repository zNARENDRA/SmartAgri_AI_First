"""
SmartAgri AI - PyTorch ResNet Model Evaluation & Agreement Layer Tests
"""

import os
import sys
import pytest
from PIL import Image
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.config import DATA_SAMPLES
from app.services.pytorch_disease_model import pytorch_disease_service, PYTORCH_PLANTVILLAGE_CLASSES
from app.services.disease_service import disease_service

@pytest.fixture
def sample_leaf_bytes():
    # Load actual sample file if present or create structured foliage leaf image
    sample_files = [f for f in os.listdir(DATA_SAMPLES) if f.endswith((".jpg", ".png"))] if os.path.exists(DATA_SAMPLES) else []
    if sample_files:
        with open(os.path.join(DATA_SAMPLES, sample_files[0]), "rb") as f:
            return f.read()
            
    import numpy as np
    np.random.seed(42)
    arr = np.zeros((224, 224, 3), dtype=np.uint8)
    arr[:, :, 0] = np.random.randint(40, 180, (224, 224)) # Red channel variation
    arr[:, :, 1] = np.random.randint(80, 240, (224, 224)) # Green channel leaf texture
    arr[:, :, 2] = np.random.randint(20, 100, (224, 224)) # Blue channel variation
    img = Image.fromarray(arr)
    buf = BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def test_pytorch_model_classes_count():
    assert len(PYTORCH_PLANTVILLAGE_CLASSES) == 38
    assert "Apple___Cedar_apple_rust" in PYTORCH_PLANTVILLAGE_CLASSES
    assert "Tomato___Bacterial_spot" in PYTORCH_PLANTVILLAGE_CLASSES

def test_pytorch_standalone_prediction(sample_leaf_bytes):
    pred = pytorch_disease_service.predict(sample_leaf_bytes)
    assert "detected_crop" in pred
    assert "condition" in pred
    assert "confidence" in pred
    assert "top_3_predictions" in pred
    assert len(pred["top_3_predictions"]) <= 3

def test_agreement_layer_consensus(sample_leaf_bytes):
    diag = disease_service.diagnose(sample_leaf_bytes, filename="rust_leaf.jpg")
    assert diag.request_id.startswith("DX-2026-")
    assert diag.debug_info is not None
    assert "model_a_prediction" in diag.debug_info
    assert "model_b_prediction" in diag.debug_info
    assert "models_agreed" in diag.debug_info
    assert diag.debug_info["model_b_prediction"]["source"] == "PyTorch ResNet9 (manthan89-py)"
