import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_cdc():
    template_path = Path(r"C:\Users\aless\.gemini\antigravity\brain\47f435d7-de23-4f73-8784-af8b905e65f7\.user_uploaded\media_1795519021774_e8f9004c.docx")
    out_path = Path(r"c:\Users\aless\Desktop\antigravity\Alessio\projet_inov\docs\CahierDesCharges_v0.docx")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    doc = docx.Document(str(template_path))
    
    # --- P36: Solutions Concurrentes ---
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "…":
            p.text = (
                "L'analyse de l'état de l'art et du marché médical révèle deux grandes familles de solutions existantes, "
                "chacune présentant des limites structurelles que PREVENT-X AI résout de manière disruptive :\n\n"
                "1. Solutions d'IA radiologique unimodales (ex: Qure.ai - qXR, Lunit - INSIGHT CXR, Milvue Suite) :\n"
                "   - Forces : Excellente sensibilité pour la détection des anomalies pulmonaires directes (nodules, condensations, pneumothorax).\n"
                "   - Faiblesses : Focalisation quasi exclusive sur la sphère pleuro-pulmonaire et oncologique. Aucune modélisation du risque "
                "cardiovasculaire ou neurovasculaire à 5 ans, et absence totale d'intégration des données biologiques/cliniques du patient.\n\n"
                "2. Calculatrices et scores de risque cliniques traditionnels (ex: ESC SCORE2, Framingham Risk Score) :\n"
                "   - Forces : Recommandés par les sociétés savantes internationales, bien intégrés dans les recommandations de cardiologie.\n"
                "   - Faiblesses : Purement statistiques et tabulaires. N'exploitent absolument pas l'imagerie thoracique pourtant disponible "
                "(calcifications de la crosse aortique, hypertrophie ventriculaire gauche et ostéopénie vertébrale restent ignorées).\n\n"
                "3. Positionnement unique et avantage concurrentiel de PREVENT-X AI :\n"
                "   - Approche Multimodale Unifiée : PREVENT-X fusionne par mécanisme de Cross-Attention l'imagerie thoracique native DICOM "
                "et le profil biologique du patient (cohorte Cleveland Clinic, 13 variables physiologiques).\n"
                "   - Dépistage Opportuniste Passif : Valorisation des radiographies de routine pour détecter des risques cardiovasculaires majeurs "
                "sans imposer d'examens invasifs ou coûteux supplémentaires.\n"
                "   - Explicabilité Clinique Certifiée : Suppression du phénomène de 'boîte noire' grâce au moteur Grad-CAM et aux intervalles "
                "de confiance à 95% ($CI_{95\\%}$)."
            )
            break

    # --- TABLE 0: Page de Garde ---
    doc.tables[0].rows[0].cells[1].text = "24/11/2026"
    doc.tables[0].rows[1].cells[1].text = "0"

    # --- TABLE 1: Identification & Équipe ---
    t1 = doc.tables[1]
    t1.rows[0].cells[4].text = "☑" # Check M1-B1
    t1.rows[1].cells[2].text = "INOV-2026-MED01"
    t1.rows[2].cells[2].text = "PREVENT-X AI"
    t1.rows[3].cells[2].text = "Alessio BAGNOL (B1 - Responsable Technique, Architecture IA & Vision par Ordinateur)"
    t1.rows[4].cells[2].text = "Membre M1 - 1 (M1 - Réglementation Médicale & Conformité MDR 2017/745 Classe IIa)"
    t1.rows[5].cells[2].text = "Membre M1 - 2 (M1 - Cybersécurité Santé HDS & Intégration SIH/PACS)"
    t1.rows[6].cells[2].text = "Membre M1 - 3 (M1 - Assurance Qualité, Risques ISO 14971 & Validation Clinique)"
    t1.rows[7].cells[2].text = "Membre M1 - 4 (M1 - Data Engineering, Normalisation & Pipelines DICOM)"

    # --- TABLE 2: Entreprise & Activité ---
    t2 = doc.tables[2]
    t2.rows[0].cells[1].text = "2026"
    t2.rows[1].cells[1].text = "MedTech & Logiciel d'Aide à la Décision Clinique (SaMD) par Intelligence Artificielle Multimodale"

    # --- TABLE 3: Logo ---
    t3 = doc.tables[3]
    t3.rows[1].cells[0].text = ""
    p_logo = t3.rows[1].cells[0].paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    logo_path = Path(r"c:\Users\aless\Desktop\antigravity\Alessio\projet_inov\assets\logos\logo_prevent_x_official_transparent.png")
    if logo_path.exists():
        run_logo = p_logo.add_run()
        run_logo.add_picture(str(logo_path), width=Inches(2.2))
        p_sub = t3.rows[1].cells[0].add_paragraph("PREVENT-X AI — Precision Biometric Core")
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub.runs[0].font.size = Pt(9)
        p_sub.runs[0].font.color.rgb = RGBColor(100, 116, 139)

    # --- TABLE 4: Description de votre Solution ---
    doc.tables[4].rows[1].cells[0].text = (
        "PREVENT-X AI est une plateforme logicielle d'aide à la décision médicale (Dispositif Médical logiciel SaMD Classe IIa "
        "selon le Règlement Européen MDR 2017/745). Elle est conçue pour le dépistage précoce et l'estimation probabiliste du risque à 5 ans "
        "de 3 pathologies majeures : les accidents cardiovasculaires graves (MACE), les accidents vasculaires cérébraux (AVC) et les fractures ostéoporotiques.\n\n"
        "La solution repose sur une architecture d'Intelligence Artificielle Multimodale fusionnant :\n"
        "1. Une branche Vision (ResNet-18 adapté aux clichés thoraciques DICOM natifs à 1 canal de niveaux de gris) extrayant "
        "les biomarqueurs radiologiques critiques (bouton et crosse aortique, indice cardiothoracique, densité osseuse vertébrale).\n"
        "2. Une branche Tabulaire (Perceptron multicouche) traitant les biomarqueurs physiologiques et anamnestiques (cohorte de référence Cleveland Clinic, 13 variables).\n"
        "3. Un goulot d'étranglement de fusion par Cross-Attention avec têtes de prédiction multi-tâches.\n"
        "4. Un moteur d'explicabilité Grad-CAM certifié générant des cartes thermiques d'activation anatomique superposées au cliché, assorties "
        "d'intervalles de confiance statistiques à 95% ($CI_{95\\%}$) et d'une empreinte cryptographique SHA-256 garantissant l'intégrité des images."
    )

    # --- TABLE 5: Valeurs véhiculées par l’entreprise ---
    doc.tables[5].rows[1].cells[0].text = (
        "1. Rigueur Médicale et Sécurité Patient : L'outil est strictement probabiliste et d'aide à la décision ; il ne se substitue "
        "jamais au médecin radiologue ou cardiologue qui conserve la responsabilité diagnostique souveraine.\n"
        "2. Transparence Algorithmique ('No Black Box') : Refus absolu de l'opacité. Chaque prédiction est obligatoirement expliquée "
        "par cartographie d'attention visuelle Grad-CAM et bornée par un intervalle de confiance à 95%.\n"
        "3. Confidentialité et Souveraineté des Données de Santé : Dé-identification stricte selon la norme DICOM PS 3.15 dès l'ingestion, "
        "hébergement agréé Données de Santé (HDS) et conformité rigoureuse avec l'Article 35 du RGPD (DPIA/AIPD).\n"
        "4. Sobriété et Efficacité Clinique : Interface pensée pour les praticiens, calquée sur les standards ergonomiques PACS/RIS "
        "(mode sombre haute lisibilité GSDF), sans animations superflues ni éléments de gamification."
    )

    # --- TABLE 6: Produit(s) et/ou Service(s) vendu(s) ---
    doc.tables[6].rows[1].cells[0].text = (
        "- Licence logicielle PREVENT-X Hospital : Déploiement sur site sécurisé (On-Premise / Cloud privé HDS) avec connecteurs PACS "
        "pour centres hospitaliers universitaires (CHU) et cliniques privées.\n"
        "- Module SaaS PREVENT-X Practice : Accès web sécurisé pour cabinets de radiologie indépendants et centres de médecine préventive, "
        "facturé à l'abonnement mensuel par praticien.\n"
        "- Passerelle d'intégration API DICOM/HL7/FHIR : Connectivité directe aux Systèmes d'Information Hospitaliers (SIH) et aux dossiers patients informatisés.\n"
        "- Service de Monitoring Continu & Surveillance Post-Commercialisation (PMS) : Détection de dérive des données (Model Drift) "
        "et rapports périodiques de sécurité (PSUR) exigés par le MDR 2017/745."
    )

    # --- TABLE 7: Analyse de l’existant ---
    doc.tables[7].rows[1].cells[0].text = (
        "En pratique clinique courante, des millions de radiographies thoraciques sont prescrites chaque année pour des motifs "
        "de routine (bilan préopératoire, toux bénigne, visite de médecine du travail). La majorité des informations cardiovasculaires "
        "silencieuses contenues dans ces clichés (calcifications aortiques débutantes, allongement de l'apex cardiaque, ostéopénie) "
        "ne sont pas systématiquement quantifiées faute de temps radiologique dédié.\n\n"
        "Les scores traditionnels (SCORE2, Framingham) n'utilisent aucune donnée d'imagerie. Inversement, les rares solutions d'IA du marché "
        "sont cantonnées à la détection de nodules pulmonaires ou fonctionnent en boîte noire fermée sans mise en corrélation biologique. "
        "PREVENT-X comble ce vide en créant un dépistage opportuniste multimodal automatisé."
    )

    # --- TABLE 8: Objectifs Qualitatifs ---
    doc.tables[8].rows[1].cells[0].text = (
        "- Zéro boîte noire : Justification visuelle de chaque score de risque par cartographie Grad-CAM sur les quadrants anatomiques réels.\n"
        "- Ergonomie clinique médicale : Respect strict des standards de visualisation PACS (Grayscale Standard Display Function - GSDF).\n"
        "- Sécurité juridique et déontologique pour le médecin : Restitution systématique des intervalles de confiance $CI_{95\\%}$ et empreinte SHA-256.\n"
        "- Dé-identification automatisée irréversible des données DICOM avant tout traitement par le réseau de neurones."
    )

    # --- TABLE 9: Objectifs Quantitatifs ---
    doc.tables[9].rows[1].cells[0].text = (
        "- Performance prédictive : AUC-ROC supérieure à 0.85 et sensibilité supérieure à 88% sur la détection des hauts risques cardiovasculaires.\n"
        "- Vitesse d'exécution : Temps d'inférence multimodale complet inférieur à 1,5 seconde par patient sur machine standard.\n"
        "- Productivité praticien : Réduction estimée de 30% du temps nécessaire au bilan radiologique préventif.\n"
        "- Taux de couverture de tests : 100% de passage sur la suite de tests unitaires et d'intégrité de données."
    )

    # --- TABLE 10: Futur(s) Utilisateur(s) de votre solution (Persona) ---
    doc.tables[10].rows[1].cells[0].text = (
        "1. Médecins Radiologues : Lecture rapide et assistée des clichés thoraciques de routine pour repérer instantanément les signes vasculaires d'alerte.\n"
        "2. Cardiologues hospitaliers et de ville : Prise en charge précoce des patients à risque cardiovasculaire élevé avant la survenue d'un infarctus.\n"
        "3. Médecins du travail et de prévention : Bilan de santé global lors des visites d'aptitude et dépistage de masse non invasif."
    )

    # --- TABLE 11: Persona détaillé ---
    t11 = doc.tables[11]
    t11.rows[0].cells[1].text = "Dr. Laurent Mercier"
    t11.rows[2].cells[0].text = (
        "- Âge : 47 ans\n"
        "- Poste : Médecin Radiologue Praticien Hospitalier (CHU) et associé en centre d'imagerie médical privé.\n"
        "- Activité : Analyse 60 à 80 clichés de radiographie par jour dans un flux de travail intense.\n"
        "- Objectif : Détecter les signaux faibles (calcifications de la crosse aortique, dilatation du ventricule gauche) sans alourdir le temps de vacation."
    )
    t11.rows[4].cells[0].text = (
        "- Exigence absolue de transparence : Refuse les solutions d'IA 'gadgets' ou fermées ; exige de voir précisément où l'IA regarde (Grad-CAM).\n"
        "- Ergonomie PACS : L'outil doit s'intégrer dans son environnement habituel (fond sombre, zéro fioritures, compte-rendu imprimable en un clic).\n"
        "- Responsabilité médicale : A besoin de connaître le degré d'incertitude ($CI_{95\\%}$) pour adapter son orientation diagnostique."
    )

    # --- TABLE 12: Clients : qui paie ? ---
    doc.tables[12].rows[1].cells[0].text = (
        "- Établissements de santé publics et privés : Groupements Hospitaliers de Territoire (GHT), Centres Hospitaliers Universitaires (CHU), cliniques privées.\n"
        "- Réseaux de centres d'imagerie médicale : Cabinets mutualisés cherchant à valoriser leurs actes de dépistage et sécuriser leurs diagnostics.\n"
        "- Compagnies d'assurance santé et mutuelles : Financement de programmes pilotes de prévention cardiovasculaire réduisant le coût des urgences AVC/infarctus."
    )

    # --- TABLE 13: Offre et prix ---
    doc.tables[13].rows[1].cells[0].text = (
        "- Offre Établissement / GHT (On-Premise / HDS privé) : Licence annuelle d'établissement à 18 000 € / an (volume illimité d'examens, support 24/7 et mises à jour de sécurité).\n"
        "- Offre Cabinet Radiologique (SaaS HDS sécurisé) : 350 € / mois par praticien actif (comprenant 500 inférences mensuelles et génération de rapports certifiés).\n"
        "- Pack Recherche Clinique & Registres : 8 000 € pour l'accès aux fonctionnalités d'analyse de cohortes et d'export de biomarqueurs de recherche."
    )

    # --- TABLE 14: Coûts et revenus estimés ---
    doc.tables[14].rows[1].cells[0].text = (
        "- Coûts prévisionnels (An 1) : Infrastructure Cloud certifiée HDS et calcul GPU (~9 600 €/an), amorçage de la démarche de certification MDR 2017/745 Classe IIa (audit ISO 13485 : ~15 000 €).\n"
        "- Revenus prévisionnels : An 1 = 72 000 € (4 établissements pilotes) ; An 2 = 270 000 € (15 établissements) ; An 3 = 650 000 € (expansion nationale).\n"
        "- Seuil de rentabilité (Break-even) : Atteint au 18ème mois d'exploitation."
    )

    # --- TABLE 15: Type de solution ---
    doc.tables[15].rows[1].cells[0].text = "☑" # Purement applicative

    # --- TABLE 16: Modèle économique ---
    doc.tables[16].rows[0].cells[0].text = "☑" # Propriétaire Payante

    # --- TABLE 17: Catégories ---
    t17 = doc.tables[17]
    t17.rows[1].cells[0].text = "☑" # Application web
    t17.rows[2].cells[3].text = "☑" # Intelligence artificielle / Data
    t17.rows[3].cells[0].text = "☑" # Cybersécurité
    t17.rows[4].cells[0].text = "☑" # Santé / Bien-être

    # --- TABLE 18: Fonctionnalités de la solution ---
    doc.tables[18].rows[1].cells[0].text = (
        "1. Ingestion DICOM native et Dé-identification automatique (conforme DICOM PS 3.15) des fichiers `.dcm` et images radiographiques.\n"
        "2. Extraction automatique des biomarqueurs radiologiques clés : Indice Cardiothoracique (RCT) et Indice de Calcification Aortique (ICA).\n"
        "3. Module d'ingestion tabulaire sécurisé des données anamnestiques et biologiques (profil de référence Cleveland Clinic).\n"
        "4. Moteur d'inférence multimodale conjointe par réseau de neurones profonds (ResNet-18 + MLP tabulaire + Cross-Attention).\n"
        "5. Cartographie d'explicabilité visuelle Grad-CAM en temps réel localisant les zones d'activation sur le bouton aortique et le ventricule gauche.\n"
        "6. Calcul statistique rigoureux des bornes d'incertitude ($CI_{95\\%}$) pour chaque prédiction de risque.\n"
        "7. Émission d'un compte-rendu radiologique officiel au format PDF médical certifié, scellé par empreinte cryptographique SHA-256."
    )

    # --- TABLE 19: Contraintes de la solution ---
    doc.tables[19].rows[1].cells[0].text = (
        "- Réglementaires : Classification Dispositif Médical logiciel SaMD Classe IIa (MDR 2017/745), respect des normes ISO 14971 (Gestion des risques) et CEI 62304 (Cycle de vie des logiciels médicaux).\n"
        "- Sécurité et Éthique : Conformité intégrale au RGPD (AIPD/DPIA Art. 35), hébergement exclusif sur serveurs certifiés HDS, anonymisation à la source.\n"
        "- Déontologiques : Non-substitution au diagnostic médical ; notification explicite que la décision thérapeutique finale relève du médecin traitant.\n"
        "- Techniques : Tolérance stricte aux faux négatifs sur les calcifications critiques et exécution sous contrainte de latence (< 1,5s)."
    )

    # --- TABLE 20: Découpage Fonctionnel ---
    doc.tables[20].rows[1].cells[0].text = (
        "- Module 1 - Ingestion & Anonymisation DICOM (`engine/analyzer.py`) : Parsing des en-têtes DICOM, suppression des identifiants patients, rehaussement de contraste CLAHE, calcul RCT et ICA.\n"
        "- Module 2 - Pipeline de Données Cliniques (`data/real_data_pipeline.py`) : Traitement de la cohorte Cleveland, normalisation statistique standardisée, split stratifié par patient.\n"
        "- Module 3 - Architecture Deep Learning Multimodale (`models/architecture.py`, `models/train.py`) : ResNet-18 monocanal, MLP 13 descripteurs, goulot de fusion Cross-Attention et têtes multi-tâches.\n"
        "- Module 4 - Moteur d'Inférence & Explicabilité (`engine/certified_inference.py`) : Rétropropagation des gradients Layer4, génération thermique Grad-CAM, intervalles $CI_{95\\%}$ et scellement SHA-256.\n"
        "- Module 5 - Générateur de Rapports Cliniques (`reports/generator.py`) : Compilation automatisée du compte-rendu d'imagerie au format PDF médical vectoriel (ReportLab).\n"
        "- Module 6 - Interface & API du Poste de Travail (`main.py`) : Serveur d'orchestration FastAPI et tableau de bord clinicien aux normes PACS/RIS."
    )

    # --- TABLE 21: Stack Technique ---
    doc.tables[21].rows[1].cells[0].text = (
        "- Langage de programmation : Python 3.12 (architecture typée et optimisée).\n"
        "- Framework Deep Learning : PyTorch 2.15 & Torchvision (modélisation neuronale, rétropropagation Grad-CAM).\n"
        "- Traitement d'imagerie médicale : pydicom (parsing DICOM PS 3.15), OpenCV (filtrage, CLAHE, masques), NumPy, SciPy.\n"
        "- Traitement tabulaire & Machine Learning : Scikit-learn (stratification, normalisation), Pandas.\n"
        "- Backend & API : FastAPI, Uvicorn, Pydantic v2.\n"
        "- Moteur d'édition documentaire : ReportLab (génération PDF vectorielle native).\n"
        "- Qualité et Tests : Unittest, Git / GitHub pour la traçabilité des versions et du modèle."
    )

    # --- TABLE 22: Sécurisation ---
    doc.tables[22].rows[1].cells[0].text = (
        "- Dé-identification conforme DICOM PS 3.15 : Anonymisation à la volée des balises nominatives (`PatientName`, `PatientID`, `BirthDate`, `InstitutionName`).\n"
        "- Traçabilité et intégrité cryptographique : Hachage SHA-256 calculé sur chaque cliché radiographique brut pour garantir l'absence d'altération en transit.\n"
        "- Chiffrement en transit et au repos : Protocole TLS 1.3 obligatoire sur tous les flux réseau et chiffrement AES-256 des volumes de données.\n"
        "- Contrôle d'accès et habilitations : Authentification forte et gestion des rôles (RBAC) pour les praticiens autorisés.\n"
        "- Hygiène de code : Exclusion absolue de tout secret ou clé API dans le dépôt de versionnement (gestion via variables d'environnement)."
    )

    # --- TABLE 23: RGPD ---
    doc.tables[23].rows[1].cells[0].text = (
        "- Analyse d'Impact relative à la Protection des Données (AIPD / DPIA) rédigée conformément à l'Article 35 du RGPD pour les données de santé à caractère sensible.\n"
        "- Principe de minimisation des données : Traitement strict des seules variables physiologiques nécessaires à l'inférence prédictive.\n"
        "- Volatilité des données d'inférence : Traitement en mémoire volatile sans stockage persistant des clichés sans consentement préalable du patient.\n"
        "- Tenue d'un registre officiel des activités de traitement et désignation d'un DPO référent."
    )

    # --- TABLE 24: Plan de tests ---
    doc.tables[24].rows[1].cells[0].text = (
        "- Suite de tests unitaires automatisée (`tests/test_prevent_x_suite.py`) validant :\n"
        "  1. L'anonymisation rigoureuse des clichés DICOM (`test_dicom_anonymization_and_metrics`).\n"
        "  2. L'exactitude et la reproductibilité du scellement cryptographique SHA-256 (`test_sha256_image_integrity_hash`).\n"
        "  3. La fidélité du pipeline de données de la cohorte Cleveland (`test_real_tabular_pipeline_data_split`).\n"
        "  4. L'intégrité de l'inférence PyTorch et des intervalles $CI_{95\\%}$ (`test_certified_pytorch_inference`).\n"
        "  5. La validité géométrique des cartes d'explicabilité Grad-CAM (`test_gradcam_heatmap_validity`).\n"
        "- Tests de non-régression et suivi de la convergence des fonctions de perte d'entraînement (Loss train < 0.75, Loss val < 0.80)."
    )

    # --- TABLE 25: Critères de réussite (recette) ---
    doc.tables[25].rows[1].cells[0].text = (
        "- 100% des tests unitaires de la suite automatisée validés avec succès sans avertissement.\n"
        "- Score diagnostique global AUC-ROC supérieur à 0.85 sur la cohorte de validation indépendante.\n"
        "- Absence d'artefact ou de gradient nul sur la cartographie Grad-CAM (activation prouvée sur les zones cibles bouton aortique et silhouette cardiaque).\n"
        "- Génération sans erreur du rapport PDF médical vectoriel scellé par l'empreinte SHA-256 en moins de 1,5 seconde."
    )

    # --- TABLE 26: Police / Typographie ---
    doc.tables[26].rows[1].cells[0].text = (
        "- Titres, labels cliniques et valeurs métriques : Inter et JetBrains Mono (lisibilité numérique optimale pour les ratios et scores).\n"
        "- Corps de texte médical et comptes-rendus : Arial / Helvetica (standards universels pour documents d'imagerie clinique)."
    )

    # --- TABLE 27: Couleurs ---
    doc.tables[27].rows[1].cells[0].text = (
        "- Fond radiologique principal : Sober Medical Dark `#090D16` / `#0F172A` (optimisé pour moniteurs de radiologie).\n"
        "- Accents fonctionnels : Cyan Médical `#0EA5E9` et Émeraude Vital `#10B981` (validation et zones stables).\n"
        "- Codes de vigilance diagnostique : Ambre de prudence `#F59E0B` (risque intermédiaire) et Rouge critique `#EF4444` (risque élevé).\n"
        "- Neutralité typographique : Blanc pur `#FFFFFF` et Gris ardoise `#94A3B8` pour un contraste optimal sans éblouissement."
    )

    # --- TABLE 28: Autres éléments graphiques ---
    doc.tables[28].rows[1].cells[0].text = (
        "- Logo officiel 'Precision Biometric Core' décliné en version couleur haute définition et en monochrome blanc pur `#FFFFFF` sur fond transparent.\n"
        "- Échelle de calibrage niveaux de gris GSDF intégrée sur la mire radiologique pour contrôle visuel immédiat du praticien."
    )

    # --- TABLE 29: Matériels et Fournitures ---
    t29 = doc.tables[29]
    t29.rows[1].cells[0].text = "Station GPU Nvidia RTX (Entraînement PyTorch & Inférence Grad-CAM)"
    t29.rows[1].cells[1].text = "Infrastructure EPSI myDiL"
    t29.rows[1].cells[2].text = "0.00 €"
    t29.rows[1].cells[3].text = "1"
    t29.rows[1].cells[4].text = "0.00 €"
    t29.rows[1].cells[5].text = "Oui (myDiL)"

    t29.rows[2].cells[0].text = "Moniteur radiologique étalonné GSDF (Contrôle qualité d'affichage)"
    t29.rows[2].cells[1].text = "Laboratoire d'innovation myDiL"
    t29.rows[2].cells[2].text = "0.00 €"
    t29.rows[2].cells[3].text = "1"
    t29.rows[2].cells[4].text = "0.00 €"
    t29.rows[2].cells[5].text = "Oui (myDiL)"

    t29.rows[3].cells[0].text = "Cohortes cliniques ouvertes certifiées (Cleveland Clinic Heart Disease & CheXpert)"
    t29.rows[3].cells[1].text = "Bases de recherche clinique publique"
    t29.rows[3].cells[2].text = "0.00 €"
    t29.rows[3].cells[3].text = "1"
    t29.rows[3].cells[4].text = "0.00 €"
    t29.rows[3].cells[5].text = "Oui"

    t29.rows[4].cells[0].text = "Environnement d'exécution Sandbox sécurisé HDS"
    t29.rows[4].cells[1].text = "Serveur académique EPSI"
    t29.rows[4].cells[2].text = "0.00 €"
    t29.rows[4].cells[3].text = "1"
    t29.rows[4].cells[4].text = "0.00 €"
    t29.rows[4].cells[5].text = "Oui"

    t29.rows[6].cells[4].text = "0.00 €"

    # --- TABLE 30: Spécificités d’exploitation ---
    doc.tables[30].rows[1].cells[0].text = (
        "- Conteneurisation Docker standardisée permettant un déploiement sécurisé sur site hospitalier ou cloud privé HDS.\n"
        "- Connectivité DICOM C-STORE / C-MOVE et API REST sécurisée pour l'interfaçage avec les serveurs PACS et dossiers patients.\n"
        "- Journalisation immuable (Audit Trail) de chaque inférence : horodatage certifié, version du checkpoint IA, score, empreinte SHA-256 du cliché."
    )

    # --- TABLE 31: Livrables ---
    doc.tables[31].rows[1].cells[0].text = (
        "- Livrable 1 : Code source complet versionné et testé sur le dépôt GitHub officiel (`alessio-bagnol/projet_inov`).\n"
        "- Livrable 2 : Modèle Deep Learning multimodal entraîné et certifié (`models/checkpoints/best_multimodal_model.pt`) avec rapport d'entraînement (`models/training_report.json`).\n"
        "- Livrable 3 : Suite de tests automatisés et pipeline de validation continue (`tests/test_prevent_x_suite.py`).\n"
        "- Livrable 4 : Dossier de spécifications architecturales et réglementaires MDR/RGPD (`docs/`).\n"
        "- Livrable 5 : Cahier des Charges officiel complet du Cycle d'Innovation (`CahierDesCharges_v0.docx`)."
    )

    # --- TABLE 32: Agenda de phases ---
    doc.tables[32].rows[1].cells[0].text = (
        "- Phase 1 (Novembre 2026 - Janvier 2027) : Cadrage médical, état de l'art, pipeline d'ingestion DICOM et intégration de la cohorte Cleveland Clinic.\n"
        "- Phase 2 (Février 2027 - Mai 2027) : Entraînement du modèle multimodal PyTorch, optimisation de la fusion Cross-Attention, moteur Grad-CAM et tests unitaires.\n"
        "- Phase 3 (Juin 2027 - Novembre 2027) : Finalisation du poste de travail clinique PACS/RIS, validation sur cohortes externes, conformité ISO 14971.\n"
        "- Phase 4 (Décembre 2027 - Juin 2028) : Dossier de marquage CE Dispositif Médical Classe IIa, tests d'interopérabilité HL7/FHIR et soutenance finale du Cycle d'Innovation."
    )

    # --- TABLE 33: Tâches attribuées aux Innov-Member ---
    doc.tables[33].rows[1].cells[0].text = (
        "- Alessio BAGNOL (B1) : Conception de l'architecture logicielle, implémentation du pipeline de données tabulaires et radiologiques, modélisation PyTorch multimodale, moteur d'explicabilité Grad-CAM, interface clinique et documentation d'ingénierie.\n"
        "- Membres M1 (Équipe M1) : Spécifications cliniques et analyse des risques médicaux (ISO 14971 / FMEA), veille réglementaire MDR 2017/745 SaMD Classe IIa, audit de conformité RGPD / HDS, protocoles de validation croisée et intégration aux architectures hospitalières SIH."
    )

    # --- TABLE 34: Outil de gestion de projet ---
    doc.tables[34].rows[1].cells[0].text = (
        "Pour assurer un suivi agile et collaboratif rigoureux du projet PREVENT-X AI sur le cycle 2026-2028, nous utilisons un tableau Trello / Notion structuré selon la méthode Scrum/Kanban (Backlog, Sprint en cours, En cours de test, Validé / Terminé).\n\n"
        "L'outil permet :\n"
        "- La traçabilité des fonctionnalités techniques (User Stories), des exigences de conformité médicale (MDR 2017/745, ISO 14971) et des jalons de livraison académiques.\n"
        "- La répartition claire des responsabilités entre les membres de l'équipe (Alessio BAGNOL en B1 et les 4 étudiants de M1).\n"
        "- Le partage transparent de l'avancement avec l'équipe pédagogique et les tuteurs myDiL.\n\n"
        "L'invitation d'accès avec droits de consultation et supervision a été formellement adressée à l'adresse de contact du laboratoire d'innovation EPSI :\n"
        "👉 mydilmontpellier34@gmail.com"
    )

    # --- TABLE 35: Risques du Projet ---
    t35 = doc.tables[35]
    risks_data = [
        ("Faux négatif critique sur pathologie aiguë (ex: calcification aortique sévère non détectée)", "Faible", "Majeur", "Calibrage d'un seuil de sensibilité élevé (>88%), alerte visuelle Grad-CAM et rappel déontologique de non-substitution au diagnostic du médecin."),
        ("Biais de représentativité dans les données d'entraînement (surreprésentation d'une tranche d'âge)", "Moyenne", "Modéré", "Diversification des cohortes (Cleveland Clinic + CheXpert), validation croisée stratifiée par patient, métriques d'équité (fairness metrics)."),
        ("Fuite de données personnelles ou identifiants patients (violation RGPD / HDS)", "Faible", "Majeur", "Dé-identification stricte à la volée selon DICOM PS 3.15 dès l'ingestion, chiffrement TLS 1.3, hachage SHA-256 de traçabilité, absence de stockage nominatif."),
        ("Dérive des performances du modèle dans le temps (Model Drift / modification des protocoles)", "Faible", "Modéré", "Implémentation d'une journalisation continue (Audit Trail), détection de dérive statistique sur les descripteurs et réentraînement supervisé périodique."),
        ("Complexité et délais de certification Dispositif Médical (Règlement MDR 2017/745 Classe IIa)", "Moyenne", "Modéré", "Alignement architectural anticipé dès la phase v0 sur les normes ISO 14971 (Gestion des risques), CEI 62304 (Cycle de vie logiciel) et traçabilité complète.")
    ]
    for idx, r_data in enumerate(risks_data):
        row = t35.rows[idx + 1]
        row.cells[0].text = r_data[0]
        row.cells[1].text = r_data[1]
        row.cells[2].text = r_data[2]
        row.cells[3].text = r_data[3]

    # --- TABLE 36: L'Usage de l'IA Générative ---
    t36 = doc.tables[36]
    genai_data = [
        ("Gemini / Antigravity Agent", "Assistance au développement de l'architecture PyTorch, pipeline de normalisation de données et Grad-CAM", "Backend & Core Deep Learning", "Alessio BAGNOL"),
        ("Gemini / Antigravity Agent", "Revue de conformité aux normes réglementaires (MDR 2017/745, ISO 14971) et structuration documentaire", "Dossier de conformité et Cahier des Charges", "Équipe projet"),
        ("Générateur d'actifs graphiques", "Conception et vectorisation du logo officiel Precision Biometric Core", "Identité visuelle et Charte graphique", "Alessio BAGNOL"),
        ("Analyseurs statiques & Linter", "Assistance à l'écriture des tests unitaires et vérification de la robustesse logicielle", "Tests & CI/CD", "Alessio BAGNOL"),
        ("Outils d'édition Markdown/PDF", "Mise en page automatique des livrables techniques et du guide médical", "Livrables académiques", "Alessio BAGNOL")
    ]
    for idx, g_data in enumerate(genai_data):
        row = t36.rows[idx + 1]
        row.cells[0].text = g_data[0]
        row.cells[1].text = g_data[1]
        row.cells[2].text = g_data[2]
        row.cells[3].text = g_data[3]

    # --- TABLE 37: Historique des versions ---
    t37 = doc.tables[37]
    t37.rows[1].cells[0].text = "0"
    t37.rows[1].cells[1].text = "24/11/2026"
    t37.rows[1].cells[2].text = "Alessio BAGNOL"
    t37.rows[1].cells[3].text = "Création et rédaction initiale complète du Cahier des Charges v0 du projet PREVENT-X AI selon le référentiel EPSI myDiL 2026-2028."

    doc.save(str(out_path))
    print(f"Cahier des Charges saved successfully to {out_path} ({out_path.stat().st_size} bytes)")

if __name__ == "__main__":
    build_cdc()
