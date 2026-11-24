# État du projet : PREVENT-X AI
*Dernière mise à jour : 24 Novembre 2026*

## 🎯 Vision & Cadrage Pédagogique (2 ans : M1 → M2)
- **Programme :** Cycle d'Innovation Digitale EPSI (myDiL) - Promotion M1/B1 (2026-2028).
- **Objectif M1 (Année 1) :** Réalisation et démonstration du **PoC (Proof of Concept) fonctionnel** au Forum de l'Innovation (Juin 2027) : soumission radio/IRM + constantes, inférence IA, heatmap Grad-CAM, dashboard clinique interactif et génération du rapport PDF médical.
- **Objectif M2 (Année 2) :** Industrialisation complète (CI/CD, conformité MDR 2017/745, sécurité des données de santé HDS/RGPD, interopérabilité PACS/DICOM).

## 🧭 Ligne directrice pour le dossier & livrables
Chaque brique développée doit directement alimenter les chapitres du Cahier des Charges (CDC) :
1. **Découpage fonctionnel & Stack :** FastAPI (Python 3.12), PyTorch (EfficientNet / ResNet), OpenCV, TailwindCSS, Chart.js, ReportLab.
2. **Sécurité & RGPD :** Anonymisation automatique des scans DICOM/PNG à la volée, zéro rétention de données nominatives sans consentement.
3. **Tests & Recette :** Tests unitaires du moteur de calcul, validation de la matrice de confusion et calibration des scores.
4. **Répartition M1 / B1 :**
   - **M1 (Innov-Leads) :** Algorithmes IA/ML, architecture de fusion multimodale, logique Grad-CAM, sécurité API.
   - **B1 (Innov-Members) :** Interface utilisateur (formulaires, jauges de risque, visionneuse), intégration PDF, tests fonctionnels.

## 📌 Assets officiels
- Logo officiel : `logo.png` et `assets/logos/logo_prevent_x_official_512x512.png` (PNG sans texte retenu).

## ⏳ Prochaine étape technique
Mise en place du socle applicatif : moteur d'analyse IA et interface clinique interactive.
