# État du projet : PREVENT-X AI
*Dernière mise à jour : 24 Novembre 2026*

## 🎯 Vision & Cadrage Pédagogique (2 ans : M1 → M2)
- **Programme :** Cycle d'Innovation Digitale EPSI (myDiL) - Promotion M1/B1 (2026-2028).
- **Objectif M1 (Année 1) :** Réalisation et démonstration du **PoC (Proof of Concept) fonctionnel** au Forum de l'Innovation (Juin 2027) : soumission radio/IRM + constantes, inférence IA, heatmap Grad-CAM, dashboard clinique interactif et génération du rapport PDF médical.
- **Objectif M2 (Année 2) :** Industrialisation complète (CI/CD, conformité MDR 2017/745, sécurité des données de santé HDS/RGPD, interopérabilité PACS/DICOM).

## 🛠️ Stack Technique & Dépendances
- **Backend / IA** : Python 3.12, FastAPI, PyTorch (EfficientNet / ResNet), OpenCV, NumPy, ReportLab, Pydicom.
- **Frontend** : Interface Web moderne réactive (HTML5, TailwindCSS, Visionneuse Grad-CAM).
- **Formats d'imagerie supportés** : Fichiers hospitaliers natifs **DICOM (`.dcm`)**, PNG, JPEG, WebP.

## 📌 Architecture & Fichiers Clés
- `logo.png` : Logo officiel validé (512x512 px).
- `assets/logos/` : Déclinaisons officielles PNG couleur et blanche monochrome transparente.
- `engine/analyzer.py` : Moteur multimodal de calcul du risque (Score2 / Framingham) + extraction des biomarqueurs (RCT, Aorte ICA, Rachis) + génération Grad-CAM.
- `reports/generator.py` : Générateur officiel de rapports PDF médicaux avec visa praticien et anonymisation RGPD.
- `templates/index.html` : Interface web clinique complète avec 4 cas de test (dont DICOM).
- `samples/sample_patient_cxr.dcm` : Vrai fichier DICOM conforme ACR/NEMA pour tests immédiats.

## ✅ Réalisations récentes
- Support natif et testé des fichiers DICOM hospitaliers (`.dcm`) avec extraction automatique des métadonnées et dé-identification RGPD.
- Bouton de démonstration DICOM en 1 clic ajouté à l'interface web.
- Serveur local FastAPI opérationnel avec rechargement à chaud (`http://127.0.0.1:8000`).
- Tous les livrables sont versionnés et synchronisés sur GitHub (`alessio-bagnol/projet_inov`).

## ⏳ Prochaine étape
Initialisation du modèle de Cahier des Charges v0 (.docx) et structuration du tableau de gestion de projet (Trello/Notion).
