"""
data/real_data_pipeline.py
Pipeline d'ingestion, de normalisation et de préparation des données médicales réelles
Supporte les cohortes tabulaires cliniques (Framingham / Cleveland) et les radiographies thoraciques
"""

import os
import json
import urllib.request
import numpy as np
import cv2
from pathlib import Path
from typing import Dict, Any, List, Tuple

class MedicalDataPipeline:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def fetch_uci_heart_dataset(self) -> Path:
        """
        Télécharge le jeu de données réel de référence de la Cleveland Clinic Foundation (UCI ML Repository)
        Contient les dossiers médicaux réels avec constantes biologiques et survenue d'événements cardiovasculaires.
        """
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
        dest_file = self.raw_dir / "cleveland_heart_disease.csv"
        
        if not dest_file.exists():
            print(f"[Pipeline] Téléchargement de la cohorte Cleveland Heart Disease...")
            req = urllib.request.Request(url, headers={'User-Agent': 'PREVENT-X-Clinical-Pipeline/1.0'})
            with urllib.request.urlopen(req) as resp, open(dest_file, "wb") as f:
                f.write(resp.read())
            print(f"[Pipeline] Téléchargé avec succès ({dest_file.stat().st_size} octets).")
        else:
            print(f"[Pipeline] Cohorte Cleveland déjà présente en cache local.")

        return dest_file

    def process_tabular_cohort(self, raw_csv_path: Path) -> Dict[str, Any]:
        """
        Nettoie, normalise et sépare les données patients réelles.
        Format standard UCI Cleveland :
        0: age, 1: sex, 2: cp, 3: trestbps (PAS), 4: chol, 5: fbs, 
        6: restecg, 7: thalach, 8: exang, 9: oldpeak, 10: slope, 
        11: ca, 12: thal, 13: target (0: sain, 1-4: pathologie coronarienne)
        """
        columns = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
                   "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]
        
        valid_rows = []
        with open(raw_csv_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 14:
                    # Remplacement des valeurs manquantes '?' par des médianes cliniques
                    row = []
                    is_valid = True
                    for i, val in enumerate(parts):
                        val = val.strip()
                        if val == "?":
                            # Imputation par défaut
                            row.append(0.0 if i in [11, 12] else 120.0)
                        else:
                            try:
                                row.append(float(val))
                            except ValueError:
                                is_valid = False
                                break
                    if is_valid:
                        valid_rows.append(row)

        arr = np.array(valid_rows, dtype=np.float32)
        print(f"[Pipeline] Lignes cliniques valides extraites : {arr.shape[0]} patients.")

        # Séparation Features (X) et Cibles (Y)
        X = arr[:, :13]
        # Binarisation de la cible : 0 = Risque faible, >= 1 = Maladie cardiovasculaire avérée
        y_cv = (arr[:, 13] > 0).astype(np.float32)

        # Calcul de cibles dérivées pour les risques vasculaires & AVC
        # Le risque d'AVC est corrélé à la pression artérielle systolique (trestbps > 140) et à l'âge (>55)
        y_stroke = ((arr[:, 3] > 140) & (arr[:, 0] > 55) & (y_cv > 0)).astype(np.float32)

        # Normalisation Z-Score (Moyenne = 0, Écart-Type = 1)
        mean_x = np.mean(X, axis=0)
        std_x = np.std(X, axis=0) + 1e-7
        X_norm = (X - mean_x) / std_x

        # Séparation Patient-Level : 70% Train, 15% Validation, 15% Test
        np.random.seed(42)
        indices = np.random.permutation(len(X_norm))
        n_train = int(0.70 * len(X_norm))
        n_val = int(0.15 * len(X_norm))

        train_idx = indices[:n_train]
        val_idx = indices[n_train:n_train + n_val]
        test_idx = indices[n_train + n_val:]

        processed_data = {
            "normalization": {
                "mean": mean_x.tolist(),
                "std": std_x.tolist(),
                "feature_names": columns[:13]
            },
            "splits": {
                "X_train": X_norm[train_idx].tolist(),
                "y_cv_train": y_cv[train_idx].tolist(),
                "y_stroke_train": y_stroke[train_idx].tolist(),
                "X_val": X_norm[val_idx].tolist(),
                "y_cv_val": y_cv[val_idx].tolist(),
                "y_stroke_val": y_stroke[val_idx].tolist(),
                "X_test": X_norm[test_idx].tolist(),
                "y_cv_test": y_cv[test_idx].tolist(),
                "y_stroke_test": y_stroke[test_idx].tolist()
            },
            "meta": {
                "total_patients": len(X_norm),
                "train_patients": len(train_idx),
                "val_patients": len(val_idx),
                "test_patients": len(test_idx),
                "cv_prevalence": float(np.mean(y_cv))
            }
        }

        output_json = self.processed_dir / "tabular_cohort_processed.json"
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(processed_data, f, indent=2)

        print(f"[Pipeline] Données tabulaires normalisées sauvegardées dans {output_json}.")
        return processed_data

    def preprocess_radiograph(self, img_path: str, target_size: Tuple[int, int] = (512, 512)) -> np.ndarray:
        """
        Préparation et standardisation stricte d'un cliché radiologique :
        1. Conversion niveaux de gris 8/16-bit
        2. Égalisation adaptative de contraste médical (CLAHE)
        3. Normalisation d'échelle et centrage statistique
        """
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"Image introuvable : {img_path}")

        # Redimensionnement haute résolution
        img_resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)

        # CLAHE (Standard de lecture radiologique pour rehausser côtes et médiastin)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img_clahe = clahe.apply(img_resized)

        # Normalisation [0.0, 1.0]
        img_float = img_clahe.astype(np.float32) / 255.0
        return img_float

if __name__ == "__main__":
    pipeline = MedicalDataPipeline()
    csv_path = pipeline.fetch_uci_heart_dataset()
    cohort = pipeline.process_tabular_cohort(csv_path)
    print("[Pipeline] Résumé cohorte :", cohort["meta"])
