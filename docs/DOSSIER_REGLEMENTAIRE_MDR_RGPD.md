# 📋 Dossier Réglementaire & Sécurité : Dispositif Médical PREVENT-X AI

> **Statut Réglementaire :** Dispositif Médical Logiciel (SaMD) • Classe IIa (Règle 11, MDR 2017/745)  
> **Normes Appliquées :** ISO 13485:2016 • ISO 14971:2019 • IEC 62304:2006 • RGPD (Art. 9 & 35)

---

## 1. Analyse des Risques Médicaux (ISO 14971:2019 - Matrice FMEA)

Toute IA médicale doit prouver que son utilisation présente un **bénéfice clinique supérieur aux risques résiduels** :

| ID Risque | Danger Identifié | Cause Possible | Sévérité (1-5) | Probabilité (1-5) | Criticité Initiale | Mesure d'Atténuation (Parade Conçue) | Criticité Résiduelle |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | **Faux Négatif** (Sous-estimation du risque d'AVC) | Artefact d'exposition ou plaque aortique non visible en projection PA | **5 (Critique)** | 2 (Faible) | **10 (Inacceptable)** | **Double Garde-Fou** : Si la tension PAS $> 150$ mmHg, le risque minimal est borné par le modèle tabulaire, même si l'image est normale. | **2 (Négligeable)** |
| **RSK-02** | **Faux Positif** (Sur-alarme injustifiée) | Sternotomie, matériel de suture métallique ou bouton de pacemaker pris pour une calcification | 3 (Moyen) | 3 (Moyen) | 9 (Moyen) | **Explicabilité Grad-CAM** : La zone d'attention s'affiche en rouge. Le praticien voit immédiatement que le signal provient d'un clip métallique et invalide l'alerte. | **3 (Acceptable)** |
| **RSK-03** | **Image Dégradée ou Inadaptée** | Cliché flou, radio pédiatrique ou mauvaise incidence (profil au lieu de face) | 3 (Moyen) | 2 (Faible) | 6 (Moyen) | **Pré-filtre d'admissibilité** : Contrôle automatique de la résolution (min $512\times 512$) et de la distribution des niveaux de gris avant inférence. | **1 (Négligeable)** |
| **RSK-04** | **Fuite de Données Nominatives** | Envoi non anonymisé de tags DICOM vers un serveur externe | 4 (Élevé) | 2 (Faible) | 8 (Moyen) | **Anonymisation stricte en mémoire** : Épuration des tags `PatientName`, `PatientID`, `BirthDate` selon le profil DICOM PS 3.15 avant tout traitement. | **1 (Négligeable)** |

---

## 2. Conformité RGPD & Hébergement des Données de Santé (HDS)

### A. Les 4 Piliers Techniques de Protection :
1. **Minimisation des Données (Art. 5 RGPD)** : Seules les 6 constantes cliniques indispensables à la formule SCORE2 sont collectées. Aucune donnée sociodémographique superflue.
2. **Désidentification Irréversible** : Dès réception du flux DICOM, les métadonnées nominatives sont purgées en mémoire vive (`io.BytesIO`).
3. **Empreinte Cryptographique SHA-256** : Chaque examen est identifié par le hash SHA-256 de ses pixels bruts, garantissant qu'aucune altération de l'image n'est intervenue entre la radiographie et le diagnostic.
4. **Mode Éphémère (Zero Data Retention)** : L'image brute n'est jamais stockée sur le disque serveur en clair. Elle est traitée en mémoire, le PDF est généré et remis au praticien, puis la session est nettoyée.

---

## 3. Plan d'Évaluation Clinique (CEP - Clinical Evaluation Plan)

### A. Objectifs de Concordance Médecin vs IA :
Pour obtenir le marquage CE Classe IIa, une étude clinique rétrospective sur cohorte multicentrique (au moins 3 centres hospitaliers différents) est planifiée :
- **Cohorte minimale :** 1 200 patients consécutifs suivis pendant 5 ans.
- **Critère de jugement principal :** Aire sous la courbe ROC (AUC-ROC) pour la prédiction combinée des événements cardiovasculaires majeurs (MACE).
- **Hypothèse de supériorité :** L'approche multimodale PREVENT-X AI doit démontrer une augmentation statistiquement significative de l'AUC-ROC ($\Delta \text{AUC} \ge +0.06$, $p < 0.01$) par rapport au calculateur SCORE2 seul.
