"""
tests/test_prevent_x_suite.py
Suite de tests unitaires et de validation clinique pour PREVENT-X AI
Vérification des pipelines de données, de l'anonymisation RGPD et de l'architecture IA
"""

import os
import sys
import unittest
from pathlib import Path

# Ajouter la racine du projet
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data.real_data_pipeline import MedicalDataPipeline
from models.architecture import MultimodalPreventXModel
from engine.analyzer import ClinicalAnalyzer
from reports.generator import ReportGenerator

class TestPreventXClinicalSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = MedicalDataPipeline()
        cls.analyzer = ClinicalAnalyzer()
        cls.report_gen = ReportGenerator()

    def test_01_real_tabular_data_pipeline(self):
        """Vérifie l'ingestion, le nettoyage et le split patient-level de la cohorte réelle"""
        csv_file = self.pipeline.fetch_uci_heart_dataset()
        self.assertTrue(csv_file.exists(), "Le fichier Cleveland Heart Disease doit exister.")
        
        cohort = self.pipeline.process_tabular_cohort(csv_file)
        meta = cohort["meta"]
        self.assertGreater(meta["total_patients"], 250, "La cohorte doit contenir plus de 250 patients réels.")
        self.assertAlmostEqual(meta["train_patients"] + meta["val_patients"] + meta["test_patients"], meta["total_patients"])
        self.assertEqual(len(cohort["normalization"]["mean"]), 13, "13 variables biologiques standardisées requises.")

    def test_02_dicom_anonymization_and_ingestion(self):
        """Vérifie que le moteur DICOM ingère le fichier .dcm et applique l'anonymisation RGPD"""
        dcm_path = "samples/sample_patient_cxr.dcm"
        if os.path.exists(dcm_path):
            img_arr, dicom_meta = self.analyzer._load_medical_image(dcm_path)
            self.assertIsNotNone(img_arr, "L'image DICOM doit être décodée en tableau numpy.")
            self.assertTrue(dicom_meta.get("anonymized"), "Les métadonnées doivent être certifiées anonymisées.")
            self.assertEqual(dicom_meta.get("body_part"), "CHEST", "La modalité doit être thoracique.")

    def test_03_multimodal_pytorch_architecture(self):
        """Vérifie la cohérence des tenseurs et des sorties du réseau de neurones multimodal"""
        import torch
        model = MultimodalPreventXModel(tabular_dim=13)
        dummy_img = torch.randn(2, 1, 256, 256)
        dummy_tab = torch.randn(2, 13)
        
        out = model(dummy_img, dummy_tab)
        self.assertEqual(out["cardiac_risk"].shape, (2, 1))
        self.assertEqual(out["stroke_risk"].shape, (2, 1))
        self.assertEqual(out["bone_risk"].shape, (2, 1))
        # Vérification des bornes de probabilité sigmoïde [0, 1]
        self.assertTrue((out["cardiac_risk"] >= 0.0).all() and (out["cardiac_risk"] <= 1.0).all())

    def test_04_clinical_analyzer_inference_and_gradcam(self):
        """Vérifie le calcul multimodal et la génération de la carte d'activation Grad-CAM"""
        test_scan = "samples/real_cxr_case1_aorta.jpg"
        if os.path.exists(test_scan):
            res = self.analyzer.analyze(test_scan, {
                "age": 61,
                "gender": "Masculin",
                "systolic_bp": 155,
                "smoker": True,
                "diabetes": False,
                "total_cholesterol": 245,
                "hdl_cholesterol": 41
            })
            scores = res["scores"]
            self.assertIn("global_risk", scores)
            self.assertIn("cardiac_risk", scores)
            self.assertIn("stroke_risk", scores)
            self.assertIn("bone_risk", scores)
            self.assertGreaterEqual(scores["global_risk"], 0.0)
            self.assertLessEqual(scores["global_risk"], 100.0)
            self.assertTrue(res["images"]["gradcam_b64"].startswith("data:image/png;base64,"))

    def test_05_pdf_medical_report_generation(self):
        """Vérifie la génération du compte-rendu médical certifié au format PDF"""
        test_scan = "samples/real_cxr_case1_aorta.jpg"
        if os.path.exists(test_scan):
            res = self.analyzer.analyze(test_scan, {
                "age": 61,
                "gender": "Masculin",
                "systolic_bp": 155,
                "smoker": True,
                "diabetes": False,
                "total_cholesterol": 245,
                "hdl_cholesterol": 41
            })
            pdf_bytes = self.report_gen.generate_pdf(res, patient_id="PX-TEST-001")
            self.assertGreater(len(pdf_bytes), 50000, "Le PDF médical doit être complet et dépasser 50 Ko.")
            self.assertTrue(pdf_bytes.startswith(b"%PDF"), "Le fichier doit avoir le magic header PDF valide.")

if __name__ == "__main__":
    unittest.main()
