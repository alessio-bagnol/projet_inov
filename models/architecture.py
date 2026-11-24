"""
models/architecture.py
Architecture Deep Learning Multimodale Certifiable pour PREVENT-X AI
Fusion d'Imagerie Thoracique (Vision CNN) et de Données Cliniques (MLP) sous PyTorch
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from typing import Dict, Tuple

class VisionBackbone(nn.Module):
    """
    Encodeur Visuel basé sur ResNet avec extraction des cartes d'activation pour Grad-CAM
    """
    def __init__(self, pretrained: bool = True):
        super().__init__()
        # Chargement de ResNet18 (léger, rapide, performant en imagerie médicale)
        weights = models.ResNet18_Weights.DEFAULT if pretrained else None
        base = models.resnet18(weights=weights)
        
        # Adaptation de la première couche pour accepter des radios monochromes (1 canal)
        self.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        with torch.no_grad():
            # Initialisation par la moyenne des 3 canaux RGB pré-entraînés
            if pretrained:
                self.conv1.weight.copy_(base.conv1.weight.mean(dim=1, keepdim=True))

        self.bn1 = base.bn1
        self.relu = base.relu
        self.maxpool = base.maxpool

        self.layer1 = base.layer1
        self.layer2 = base.layer2
        self.layer3 = base.layer3
        self.layer4 = base.layer4  # Couche cible pour l'extraction Grad-CAM

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.feature_dim = 512

        # Variables pour les hooks Grad-CAM
        self.gradients = None
        self.activations = None

    def activations_hook(self, grad):
        self.gradients = grad

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        
        # Couche 4 (dernière couche convolutive riche en sémantique anatomique)
        conv_features = self.layer4(x)
        
        if conv_features.requires_grad:
            h = conv_features.register_hook(self.activations_hook)
        self.activations = conv_features

        # Pooling global
        pooled = self.avgpool(conv_features)
        embeddings = torch.flatten(pooled, 1)
        return embeddings, conv_features


class ClinicalTabularEncoder(nn.Module):
    """
    Réseau Perceptron Multicouche (MLP) régularisé pour les constantes biologiques & facteurs de risque
    """
    def __init__(self, in_features: int = 13, embed_dim: int = 64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, 128),
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Dropout(0.2),
            nn.Linear(128, embed_dim),
            nn.LayerNorm(embed_dim),
            nn.GELU()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class MultimodalPreventXModel(nn.Module):
    """
    Modèle Multi-Tâches complet avec Goulot de Fusion Multimodale
    """
    def __init__(self, tabular_dim: int = 13, vision_dim: int = 512, tabular_embed_dim: int = 64):
        super().__init__()
        self.vision_encoder = VisionBackbone(pretrained=False)
        self.tabular_encoder = ClinicalTabularEncoder(in_features=tabular_dim, embed_dim=tabular_embed_dim)

        # Fusion Bottleneck
        combined_dim = vision_dim + tabular_embed_dim
        self.fusion_layer = nn.Sequential(
            nn.Linear(combined_dim, 256),
            nn.LayerNorm(256),
            nn.GELU(),
            nn.Dropout(0.25),
            nn.Linear(256, 128),
            nn.LayerNorm(128),
            nn.GELU()
        )

        # Têtes de prédiction multi-tâches
        self.head_cardiac = nn.Linear(128, 1)   # Risque cardiaque 5 ans (Logits)
        self.head_stroke = nn.Linear(128, 1)    # Risque AVC 5 ans (Logits)
        self.head_bone = nn.Linear(128, 1)      # Score anomalie osseuse (Logits)
        self.head_biomarkers = nn.Linear(128, 3) # RCT, ACI, VBAI (Régression continue)

    def forward(self, img: torch.Tensor, tabular: torch.Tensor) -> Dict[str, torch.Tensor]:
        v_emb, conv_feats = self.vision_encoder(img)
        t_emb = self.tabular_encoder(tabular)

        # Concaténation multimodale
        combined = torch.cat([v_emb, t_emb], dim=1)
        fused = self.fusion_layer(combined)

        # Prédictions
        cardiac_prob = torch.sigmoid(self.head_cardiac(fused))
        stroke_prob = torch.sigmoid(self.head_stroke(fused))
        bone_prob = torch.sigmoid(self.head_bone(fused))
        biomarkers_pred = self.head_biomarkers(fused)

        return {
            "cardiac_risk": cardiac_prob,
            "stroke_risk": stroke_prob,
            "bone_risk": bone_prob,
            "biomarkers": biomarkers_pred,
            "features": fused
        }

if __name__ == "__main__":
    model = MultimodalPreventXModel()
    dummy_img = torch.randn(2, 1, 512, 512)
    dummy_tab = torch.randn(2, 13)
    out = model(dummy_img, dummy_tab)
    print("[Architecture] Output shapes:")
    print(" - Cardiac risk :", out["cardiac_risk"].shape)
    print(" - Stroke risk  :", out["stroke_risk"].shape)
    print(" - Bone risk    :", out["bone_risk"].shape)
    print(" - Biomarkers   :", out["biomarkers"].shape)
