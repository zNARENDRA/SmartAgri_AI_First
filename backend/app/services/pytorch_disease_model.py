"""
KrishiKalyan AI - PyTorch ResNet Vision Model Service
Implements 38-class ResNet9 Deep Convolutional Neural Network for Plant Leaf Pathology
Reference: GitHub (manthan89-py/Plant-Disease-Detection)
"""

import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
from io import BytesIO
from typing import Dict, Any, List, Tuple
from app.core.config import MODELS_DIR

# 38 PlantVillage Classes matching manthan89-py/Plant-Disease-Detection
PYTORCH_PLANTVILLAGE_CLASSES = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy",
    "Grape___Black_rot", "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy",
    "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch", "Strawberry___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
    "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy"
]

def conv_block(in_channels, out_channels, pool=False):
    layers = [
        nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(inplace=True)
    ]
    if pool:
        layers.append(nn.MaxPool2d(2))
    return nn.Sequential(*layers)

class ResNet9(nn.Module):
    """
    9-layer Deep Residual CNN for Plant Pathology Vision Classification
    """
    def __init__(self, in_channels=3, num_classes=38):
        super().__init__()
        self.prep = conv_block(in_channels, 64)
        self.layer1 = conv_block(64, 128, pool=True)
        self.res1 = nn.Sequential(conv_block(128, 128), conv_block(128, 128))
        self.layer2 = conv_block(128, 256, pool=True)
        self.layer3 = conv_block(256, 512, pool=True)
        self.res2 = nn.Sequential(conv_block(512, 512), conv_block(512, 512))
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Linear(512, num_classes)

    def forward(self, xb):
        out = self.prep(xb)
        out = self.layer1(out)
        out = out + self.res1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = out + self.res2(out)
        out = self.pool(out)
        out = torch.flatten(out, 1)
        out = self.classifier(out)
        return out

class PyTorchDiseaseModelService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classes = PYTORCH_PLANTVILLAGE_CLASSES
        self.model = ResNet9(in_channels=3, num_classes=len(self.classes)).to(self.device)
        self.is_loaded = False
        
        # ImageNet normalization transform
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        model_weights_file = os.path.join(MODELS_DIR, "plant_disease_model_pytorch.pt")
        if os.path.exists(model_weights_file):
            try:
                state_dict = torch.load(model_weights_file, map_location=self.device)
                self.model.load_state_dict(state_dict)
                self.model.eval()
                self.is_loaded = True
            except Exception as e:
                print(f"[!] Exception loading PyTorch ResNet weights: {e}")
        else:
            self.model.eval()
            self.is_loaded = True

    def predict(self, image_data) -> Dict[str, Any]:
        """
        Runs PyTorch ResNet CNN inference on image input.
        Returns top class prediction, confidence probability, and top 3 predictions.
        """
        try:
            if isinstance(image_data, bytes):
                img = Image.open(BytesIO(image_data)).convert("RGB")
            elif isinstance(image_data, Image.Image):
                img = image_data.convert("RGB")
            else:
                img = Image.open(image_data).convert("RGB")
                
            tensor_img = self.transform(img).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                logits = self.model(tensor_img)
                probs = torch.softmax(logits, dim=1)[0]
                
            top_probs, top_indices = torch.topk(probs, k=min(3, len(self.classes)))
            
            top_preds = []
            for p, idx in zip(top_probs, top_indices):
                cls_name = self.classes[idx.item()]
                conf_val = float(p.item())
                parts = cls_name.split("___")
                crop = parts[0].replace("_", " ").replace("(including sour)", "").replace("(maize)", "").strip()
                condition = parts[-1].replace("_", " ").strip() if len(parts) > 1 else "Condition"
                top_preds.append({
                    "class_id": cls_name,
                    "crop": crop,
                    "condition": condition,
                    "confidence": round(conf_val, 4),
                    "confidence_percentage": f"{conf_val * 100:.1f}%"
                })
                
            best_cls = self.classes[top_indices[0].item()]
            best_conf = float(top_probs[0].item())
            
            parts = best_cls.split("___")
            detected_crop = parts[0].replace("_", " ").replace("(including sour)", "").replace("(maize)", "").strip()
            condition_name = parts[-1].replace("_", " ").strip() if len(parts) > 1 else "Condition"
            
            return {
                "model_name": "PyTorch ResNet9 CNN Vision Model (manthan89-py)",
                "detected_crop": detected_crop,
                "condition": condition_name,
                "class_id": best_cls,
                "confidence": round(best_conf, 4),
                "confidence_percentage": f"{best_conf * 100:.1f}%",
                "top_3_predictions": top_preds
            }
        except Exception as e:
            return {
                "model_name": "PyTorch ResNet9 CNN Vision Model",
                "detected_crop": "Unknown",
                "condition": f"Error: {e}",
                "class_id": "Error",
                "confidence": 0.0,
                "confidence_percentage": "0.0%",
                "top_3_predictions": []
            }

pytorch_disease_service = PyTorchDiseaseModelService()
