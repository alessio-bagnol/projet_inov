"""
reports/generator.py
Générateur de Comptes-Rendus Médicaux Officiels au format PDF pour PREVENT-X AI
Utilise ReportLab avec intégration du logo officiel, des scores et des cartes Grad-CAM
"""

import os
import io
import time
import base64
from typing import Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image as PILImage

class ReportGenerator:
    def __init__(self, logo_path: str = None):
        self.logo_path = logo_path or r"c:\Users\aless\Desktop\antigravity\Alessio\projet_inov\logo.png"

    def generate_pdf(self, analysis_result: Dict[str, Any], patient_id: str = "PX-2026-8491", 
                     doctor_name: str = "Dr. A. Bagnol") -> bytes:
        """
        Génère un PDF médical complet en mémoire (bytes)
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Styles personnalisés
        primary_color = colors.HexColor("#0F172A")
        accent_blue = colors.HexColor("#0284C7")
        border_color = colors.HexColor("#E2E8F0")

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=primary_color
        )

        subtitle_style = ParagraphStyle(
            'DocSubTitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#64748B")
        )

        section_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=accent_blue,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#1E293B")
        )

        story = []

        # --- 1. En-tête : Logo + Titre + Métadonnées ---
        logo_flowable = ""
        if os.path.exists(self.logo_path):
            logo_flowable = RLImage(self.logo_path, width=48, height=48)

        header_text = [
            Paragraph("<b>PREVENT-X AI</b> • Clinical Decision Support", title_style),
            Paragraph("RAPPORT CLINIQUE D'ESTIMATION DU RISQUE CARDIOVASCULAIRE, AVC & OSSEUX (5 ANS)", subtitle_style),
            Paragraph("Conformité RGPD & Dispositifs Médicaux (EU MDR 2017/745 - Aide au diagnostic)", subtitle_style)
        ]

        header_table = Table([[logo_flowable, header_text]], colWidths=[56, 460])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(header_table)
        story.append(HRFlowable(width="100%", thickness=1.5, color=accent_blue, spaceAfter=10, spaceBefore=6))

        # --- 2. Bloc Patient & Données de l'Examen ---
        now_str = time.strftime("%d/%m/%Y à %H:%M")
        scores = analysis_result["scores"]
        cdata = analysis_result["clinical_data"]

        exam_meta = [
            [
                Paragraph(f"<b>ID Dossier :</b> {patient_id}", body_style),
                Paragraph(f"<b>Date de l'examen :</b> {now_str}", body_style),
                Paragraph(f"<b>Praticien :</b> {doctor_name}", body_style)
            ],
            [
                Paragraph(f"<b>Âge :</b> {cdata['age']} ans | <b>Sexe :</b> {cdata['gender']}", body_style),
                Paragraph(f"<b>Tension (PAS) :</b> {cdata['systolic_bp']} mmHg", body_style),
                Paragraph(f"<b>Fumeur :</b> {'Oui' if cdata['smoker'] else 'Non'} | <b>Diabète :</b> {'Oui' if cdata['diabetes'] else 'Non'}", body_style)
            ]
        ]
        meta_table = Table(exam_meta, colWidths=[170, 170, 176])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 1, border_color),
            ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 12))

        # --- 3. Synthèse des Risques Prédictifs à 5 Ans ---
        story.append(Paragraph("1. SYNTHÈSE DES RISQUES PRÉDICTIFS MULTIMODAUX (5 ANS)", section_style))
        
        tier_color_hex = scores["risk_color"]
        tier_color = colors.HexColor(tier_color_hex)

        ci_text = ""
        if "confidence_interval_95" in scores:
            ci = scores["confidence_interval_95"]
            ci_text = f"<br/><font size=7 color='#64748B'>IC 95%: [{ci[0]}% - {ci[1]}%]</font>"

        scores_summary_data = [
            [
                Paragraph("<b>SCORE DE RISQUE GLOBAL</b>", ParagraphStyle('W1', parent=body_style, fontName='Helvetica-Bold', fontSize=10)),
                Paragraph("<b>RISQUE CARDIAQUE</b>", ParagraphStyle('W2', parent=body_style, fontName='Helvetica-Bold')),
                Paragraph("<b>RISQUE D'AVC</b>", ParagraphStyle('W3', parent=body_style, fontName='Helvetica-Bold')),
                Paragraph("<b>ANOMALIES OSSEUSES</b>", ParagraphStyle('W4', parent=body_style, fontName='Helvetica-Bold'))
            ],
            [
                Paragraph(f"<font size=18 color='{tier_color_hex}'><b>{scores['global_risk']}%</b></font><br/>"
                          f"<font size=8.5><b>Palier : {scores['risk_tier']}</b></font>{ci_text}", body_style),
                Paragraph(f"<font size=14 color='#0284C7'><b>{scores['cardiac_risk']}%</b></font><br/>"
                          f"<font size=8 color='#64748B'>Coronarien & myocarde</font>", body_style),
                Paragraph(f"<font size=14 color='#7C3AED'><b>{scores['stroke_risk']}%</b></font><br/>"
                          f"<font size=8 color='#64748B'>Vasculaire cérébral</font>", body_style),
                Paragraph(f"<font size=14 color='#0D9488'><b>{scores['bone_risk']}%</b></font><br/>"
                          f"<font size=8 color='#64748B'>Densité & tassements</font>", body_style)
            ]
        ]
        scores_table = Table(scores_summary_data, colWidths=[150, 122, 122, 122])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#EFF6FF")),
            ('BACKGROUND', (1,0), (-1,-1), colors.HexColor("#FFFFFF")),
            ('BOX', (0,0), (-1,-1), 1, border_color),
            ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(scores_table)
        story.append(Spacer(1, 14))

        # --- 4. Biomarqueurs Quantitatifs d'Imagerie ---
        story.append(Paragraph("2. BIOMARQUEURS EXTRAITS DE L'IMAGERIE MÉDICALE", section_style))
        bio = analysis_result["biomarkers"]
        bio_data = [
            ["Biomarqueur Calculé", "Valeur Mesurée", "Plage Normative", "Interprétation Clinique"],
            [
                "Rapport Cardio-Thoracique (RCT)",
                f"{bio['cardiothoracic_ratio']}",
                "< 0.50",
                "Cardiomégalie suspectée" if bio['cardiomegaly'] else "Silhouette normale"
            ],
            [
                "Indice Calcification Aortique (ICA)",
                f"{bio['aortic_calcification_index']} / 1.0",
                "< 0.40",
                "Plaques aortiques denses" if bio['aortic_calcification_detected'] else "Paroi aortique souple"
            ],
            [
                "Score d'Atténuation Rachidienne",
                f"{bio['bone_attenuation_score']} / 1.0",
                "< 0.45",
                "Suspicion d'ostéopénie" if bio['osteopenia_suspected'] else "Densité normale"
            ]
        ]
        bio_table = Table(bio_data, colWidths=[150, 95, 95, 176])
        bio_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
            ('TEXTCOLOR', (0,0), (-1,0), primary_color),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 8.5),
            ('BOTTOMPADDING', (0,0), (-1,0), 5),
            ('BOX', (0,0), (-1,-1), 1, border_color),
            ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,1), (-1,-1), 4),
            ('BOTTOMPADDING', (0,1), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ]))
        story.append(bio_table)
        story.append(Spacer(1, 14))

        # --- 5. Imagerie & Explicabilité Grad-CAM ---
        story.append(Paragraph("3. EXPLICABILITÉ DE L'IA (GRAD-CAM DUAL VIEW)", section_style))
        
        # Sauvegarder temporairement les images à partir de base64 pour ReportLab
        raw_b64 = analysis_result["images"]["raw_b64"].split(",", 1)[1]
        cam_b64 = analysis_result["images"]["gradcam_b64"].split(",", 1)[1]

        raw_bytes = io.BytesIO(base64.b64decode(raw_b64))
        cam_bytes = io.BytesIO(base64.b64decode(cam_b64))

        img_raw_flow = RLImage(raw_bytes, width=170, height=170)
        img_cam_flow = RLImage(cam_bytes, width=170, height=170)

        img_table = Table([
            [Paragraph("<b>Radio Thoracique Brute</b>", body_style), Paragraph("<b>Carte d'Explicabilité Grad-CAM</b>", body_style)],
            [img_raw_flow, img_cam_flow],
            [
                Paragraph("<font size=7.5 color='#64748B'>Examen anonymisé à la volée (RGPD)</font>", body_style),
                Paragraph("<font size=7.5 color='#64748B'>Rouge/Jaune : zones déterminantes de l'estimation</font>", body_style)
            ]
        ], colWidths=[258, 258])
        img_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(img_table)
        story.append(Spacer(1, 12))

        # --- 6. Conclusions Cliniques & Visa Médical ---
        story.append(Paragraph("4. OBSERVATIONS ET VALIDATION MÉDICALE", section_style))
        obs_text = "<b>Conclusions générées :</b><br/>"
        for finding in analysis_result["findings"]:
            obs_text += f"• {finding}<br/>"
        
        signature_block = [
            [
                Paragraph(obs_text, body_style),
                Paragraph("<b>VISA & SIGNATURE DU PRATICIEN :</b><br/><br/><br/>"
                          "<font size=8 color='#94A3B8'>Ce document constitue un support technique d'aide à la décision. "
                          "Le diagnostic final et la prescription relèvent exclusivement du praticien responsable.</font>", body_style)
            ]
        ]
        sig_table = Table(signature_block, colWidths=[316, 200])
        sig_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, border_color),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('BACKGROUND', (1,0), (1,0), colors.HexColor("#F8FAFC")),
        ]))
        story.append(KeepTogether([sig_table]))

        # Construction du PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

if __name__ == "__main__":
    from engine.analyzer import ClinicalAnalyzer
    analyzer = ClinicalAnalyzer()
    res = analyzer.analyze(
        r"c:\Users\aless\Desktop\antigravity\Alessio\projet_inov\samples\sample_case1_aortic.png",
        {"age": 62, "systolic_bp": 155, "smoker": True, "diabetes": False, "total_cholesterol": 240, "hdl_cholesterol": 42}
    )
    gen = ReportGenerator()
    pdf = gen.generate_pdf(res)
    out_pdf = r"c:\Users\aless\Desktop\antigravity\Alessio\projet_inov\reports\test_medical_report.pdf"
    with open(out_pdf, "wb") as f:
        f.write(pdf)
    print("Report generated successfully at:", out_pdf)
