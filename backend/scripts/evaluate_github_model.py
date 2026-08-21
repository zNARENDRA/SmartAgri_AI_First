"""
SmartAgri AI - Standalone Plant Disease Model Evaluation & Benchmark Script
Evaluates:
  - Model A (Primary Engine): Multi-Scale Vision Model (plant_disease_model.joblib)
  - Model B (Secondary Engine): PyTorch ResNet9 CNN Model (manthan89-py)
"""

import os
import sys
import time
from PIL import Image
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.config import DATA_SAMPLES
from app.services.disease_service import disease_service
from app.services.pytorch_disease_model import pytorch_disease_service

def evaluate_models_side_by_side():
    print("=========================================================================")
    print("      SmartAgri AI — PLANT DISEASE VISION ENGINE BENCHMARK")
    print("=========================================================================")
    print("Comparing:")
    print("  [Model A]: Multi-Scale Vision Engine (plant_disease_model.joblib)")
    print("  [Model B]: PyTorch ResNet9 Deep CNN (manthan89-py/Plant-Disease-Detection)")
    print("=========================================================================\n")
    
    sample_files = [f for f in os.listdir(DATA_SAMPLES) if f.endswith((".jpg", ".png"))]
    if not sample_files:
        print("[!] No sample images found in data/samples.")
        return

    results_table = []
    
    for sf in sample_files:
        filepath = os.path.join(DATA_SAMPLES, sf)
        with open(filepath, "rb") as f:
            img_bytes = f.read()
            
        t0 = time.time()
        diag_a = disease_service.diagnose(img_bytes, filename=sf)
        lat_a = (time.time() - t0) * 1000
        
        t0 = time.time()
        diag_b = pytorch_disease_service.predict(img_bytes)
        lat_b = (time.time() - t0) * 1000
        
        crop_a = diag_a.detected_crop
        cond_a = diag_a.condition
        conf_a = diag_a.confidence_percentage

        
        crop_b = diag_b["detected_crop"]
        cond_b = diag_b["condition"]
        conf_b = diag_b["confidence_percentage"]
        
        agreed = (crop_a.lower() in crop_b.lower() or crop_b.lower() in crop_a.lower())
        
        results_table.append({
            "filename": sf,
            "model_a_crop": crop_a,
            "model_a_cond": cond_a,
            "model_a_conf": conf_a,
            "lat_a_ms": f"{lat_a:.1f}ms",
            "model_b_crop": crop_b,
            "model_b_cond": cond_b,
            "model_b_conf": conf_b,
            "lat_b_ms": f"{lat_b:.1f}ms",
            "agreement": "YES (Consensus)" if agreed else "NO (Disagreement)"
        })

    print(f"{'IMAGE':<20} | {'MODEL A (PRIMARY)':<30} | {'MODEL B (PYTORCH)':<30} | {'AGREEMENT':<15}")
    print("-" * 105)
    for r in results_table:
        a_str = f"{r['model_a_crop']} ({r['model_a_conf']})"
        b_str = f"{r['model_b_crop']} ({r['model_b_conf']})"
        print(f"{r['filename']:<20} | {a_str:<30} | {b_str:<30} | {r['agreement']:<15}")

    print("\n=========================================================================")
    print(f"Benchmark completed across {len(sample_files)} evaluation leaf images.")
    print("=========================================================================")

if __name__ == "__main__":
    evaluate_models_side_by_side()
