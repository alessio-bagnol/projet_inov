# État du projet : PREVENT-X AI
*Dernière mise à jour : 24 Novembre 2026 - 15:30*

## 🎯 Objectif Global & Cadrage Pédagogique (2 ans : M1 → M2)
- **Programme :** Cycle d'Innovation Digitale EPSI (myDiL) - Promotion M1/B1 (2026-2028).
- **Projet :** PREVENT-X AI — Dispositif Médical logiciel SaMD Classe IIa (Règlement Européen MDR 2017/745).
- **Mission :** Dépistage précoce opportuniste et estimation à 5 ans du risque cardiovasculaire (MACE), neurovasculaire (AVC) et ostéoporotique par fusion multimodale d'imagerie thoracique DICOM et de données physiologiques tabulaires.
- **Rôles :** Alessio BAGNOL (B1 - Responsable Technique, Architecture IA & Vision par Ordinateur) et 4 étudiants de M1 (Réglementation MDR, Cybersécurité HDS, Validation Clinique, Intégration SIH/PACS).

## 🛠️ Stack Technique & Prérequis
- **Langage & Deep Learning :** Python 3.12, PyTorch 2.15 (ResNet-18 monocanal + Tabular MLP + Cross-Attention Fusion), Torchvision.
- **Imagerie Médicale & DICOM :** pydicom (PS 3.15), OpenCV (filtrage, CLAHE, masques), NumPy, SciPy, Scikit-learn, Pandas.
- **Backend & Inférence :** FastAPI, Uvicorn, Pydantic v2.
- **Rapports & Documentation :** ReportLab (PDF vectoriel), python-docx.
- **Sécurité :** Dé-identification DICOM PS 3.15, scellement d'intégrité SHA-256, conformité RGPD Art. 35 (DPIA), secrets hors dépôt.

## 📌 Architecture & Fichiers Clés
- `logo.png` & `assets/logos/` : Logo officiel "Precision Biometric Core" (couleur HD et monochrome blanc pur transparent).
- `data/real_data_pipeline.py` : Ingestion et normalisation de la cohorte réelle Cleveland Clinic (303 patients, split stratifié 70/15/15).
- `models/architecture.py` : Architecture neuronale multimodale PyTorch avec Cross-Attention et têtes multi-tâches.
- `models/train.py` : Script d'entraînement avec suivi de perte et validation croisée.
- `models/checkpoints/best_multimodal_model.pt` : Poids du modèle entraîné certifié.
- `engine/certified_inference.py` : Moteur d'inférence certifié (Grad-CAM Layer4, $CI_{95\%}$, empreinte SHA-256).
- `engine/analyzer.py` : Ingestion native DICOM, dé-identification automatique, calcul des biomarqueurs (RCT, ICA Aorte).
- `reports/generator.py` : Générateur de compte-rendu d'imagerie PDF médical avec overlays et métadonnées d'audit.
- `docs/CahierDesCharges_v0.docx` : Cahier des Charges officiel complet généré sur le template institutionnel EPSI myDiL.
- `docs/GUIDE_MEDECINE_POUR_DEBUTANT.pdf` : Guide médical illustré et vulgarisé pour débutant (analogies plomberie et moteur).
- `docs/DOSSIER_REGLEMENTAIRE_MDR_RGPD.md` : Matrice FMEA ISO 14971, plan DPIA RGPD Art. 35 et évaluation clinique.
- `tests/test_prevent_x_suite.py` : Suite complète de tests unitaires automatisés (5/5 tests validés).

## ✅ Réalisations récentes
1. **Pipeline de données réelles :** Ingestion réussie de la cohorte Cleveland Clinic Heart Disease (303 patients, 13 variables physiologiques normalisées).
2. **Entraînement Deep Learning :** Modèle multimodal PyTorch entraîné avec succès (Loss train : 1.0027 → 0.7001 ; Loss val : 0.9677 → 0.7862).
3. **Explicabilité Grad-CAM certifiée :** Rétropropagation de gradient sur Layer4 pour activation visuelle sur le bouton aortique et le ventricule gauche, avec calcul d'intervalles $CI_{95\%}$.
4. **Validation des tests :** 100% de passage sur la suite `test_prevent_x_suite.py` (5/5 OK en 1.288s).
5. **Cahier des Charges EPSI officiel :** Remplissage intégral des 38 tableaux et chapitres du modèle institutionnel `CahierDesCharges_v0.docx`.
6. **Sécurisation & RGPD :** Dé-identification DICOM PS 3.15, hachage SHA-256 et dossier réglementaire MDR Classe IIa rédigé.

## ⏳ Prochaine étape immédiate (Action prioritaire)
Présentation du document `CahierDesCharges_v0.docx` et du tableau de gestion de projet (Trello/Notion) aux tuteurs myDiL (`mydilmontpellier34@gmail.com`) et aux membres de l'équipe M1.

## 🔒 Sécurité & Environnement
Toutes les données de santé traitées sont pseudonymisées à la volée. Aucun secret d'environnement ni donnée nominative n'est versionné sur Git.
