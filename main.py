"""
main.py - Serveur FastAPI pour PREVENT-X AI
Plateforme d'Aide à la Décision Clinique Multimodale (M1/B1 EPSI myDiL)
"""

import os
import sys
import json
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.analyzer import ClinicalAnalyzer
from reports.generator import ReportGenerator

app = FastAPI(
    title="PREVENT-X AI",
    description="Dispositif Médical d'Aide à la Décision Clinique - Dépistage Prédictif Cardiovasculaire & AVC",
    version="1.0.0"
)

# Montage des dossiers statiques
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/assets", StaticFiles(directory=str(BASE_DIR / "assets")), name="assets")
app.mount("/samples", StaticFiles(directory=str(BASE_DIR / "samples")), name="samples")

analyzer = ClinicalAnalyzer()
report_gen = ReportGenerator(logo_path=str(BASE_DIR / "logo.png"))

# Cas pré-embarqués pour démonstration immédiate
PRESET_CASES = {
    "case1": {
        "title": "Cas 1 : Homme 61 ans - Risque Vasculaire & AVC Élevé",
        "description": "Fumeur actif, hypertension modérée (155 mmHg). Détection précoce d'une calcification de la paroi aortique.",
        "sample_file": "samples/sample_case1_aortic.png",
        "clinical_data": {
            "age": 61,
            "gender": "Masculin",
            "systolic_bp": 155,
            "smoker": True,
            "diabetes": False,
            "total_cholesterol": 245,
            "hdl_cholesterol": 41
        }
    },
    "case2": {
        "title": "Cas 2 : Femme 48 ans - Examen de Routine Sain",
        "description": "Non-fumeuse, bilan pré-opératoire. Pas de calcification aortique, silhouette cardiaque harmonieuse.",
        "sample_file": "samples/sample_case2_normal.png",
        "clinical_data": {
            "age": 48,
            "gender": "Féminin",
            "systolic_bp": 118,
            "smoker": False,
            "diabetes": False,
            "total_cholesterol": 185,
            "hdl_cholesterol": 62
        }
    },
    "case3": {
        "title": "Cas 3 : Femme 72 ans - Cardiomégalie & Ostéopénie",
        "description": "Diabétique traitée. Élargissement cardiaque (RCT > 0.55) et radiotransparence accrue du rachis dorsal.",
        "sample_file": "samples/sample_case3_cardiomegaly_bone.png",
        "clinical_data": {
            "age": 72,
            "gender": "Féminin",
            "systolic_bp": 142,
            "smoker": False,
            "diabetes": True,
            "total_cholesterol": 215,
            "hdl_cholesterol": 48
        }
    },
    "case_dicom": {
        "title": "Fichier DICOM (.dcm) Réel • Examen Hospitalier",
        "description": "Fichier brut au standard DICOM 3.0 avec déchiffrement des tags et anonymisation RGPD automatique.",
        "sample_file": "samples/sample_patient_cxr.dcm",
        "clinical_data": {
            "age": 61,
            "gender": "Masculin",
            "systolic_bp": 150,
            "smoker": True,
            "diabetes": False,
            "total_cholesterol": 238,
            "hdl_cholesterol": 43
        }
    }
}

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = BASE_DIR / "templates" / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Page d'accueil non trouvée")
    return index_path.read_text(encoding="utf-8")

@app.get("/api/presets")
async def get_presets():
    return PRESET_CASES

@app.post("/api/analyze")
async def analyze_patient(
    file: Optional[UploadFile] = File(None),
    preset_key: Optional[str] = Form(None),
    patient_json: str = Form(...)
):
    try:
        patient_data = json.loads(patient_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Données patient JSON invalides: {e}")

    # Récupération de l'image (soit upload, soit cas pré-embarqué)
    img_bytes = None
    if file and file.filename:
        img_bytes = await file.read()
    elif preset_key and preset_key in PRESET_CASES:
        sample_path = BASE_DIR / PRESET_CASES[preset_key]["sample_file"]
        if sample_path.exists():
            img_bytes = sample_path.read_bytes()
    
    if not img_bytes:
        # Fallback sur le cas 1 si rien n'est fourni
        sample_path = BASE_DIR / "samples" / "sample_case1_aortic.png"
        img_bytes = sample_path.read_bytes()

    try:
        result = analyzer.analyze(img_bytes, patient_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse: {str(e)}")

class PDFRequest(BaseModel):
    analysis_result: Dict[str, Any]
    patient_id: Optional[str] = "PX-2026-8491"
    doctor_name: Optional[str] = "Dr. A. Bagnol"

@app.post("/api/export-pdf")
async def export_pdf(payload: PDFRequest):
    try:
        pdf_bytes = report_gen.generate_pdf(
            analysis_result=payload.analysis_result,
            patient_id=payload.patient_id,
            doctor_name=payload.doctor_name
        )
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=prevent_x_rapport_{payload.patient_id}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de génération PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
