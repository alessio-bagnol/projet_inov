"""
docs/generate_beginner_guide_pdf.py
Génère le guide médical ultra-pédagogique en PDF pour PREVENT-X AI
Expliqué simplement sans jargon médical pour débutant complet.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def build_pdf(output_pdf_path: str):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Palette graphique
    c_primary = colors.HexColor("#0F172A")    # Ardoise foncée
    c_blue = colors.HexColor("#0284C7")       # Cyan médical
    c_red = colors.HexColor("#DC2626")        # Rouge alerte
    c_green = colors.HexColor("#16A34A")      # Vert
    c_purple = colors.HexColor("#7C3AED")     # Violet
    c_bg_light = colors.HexColor("#F8FAFC")   # Fond carte
    c_border = colors.HexColor("#E2E8F0")

    # Typographies
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=c_primary)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=c_blue, spaceBefore=8, spaceAfter=4)
    h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=c_primary, spaceBefore=4, spaceAfter=2)
    body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13.5, textColor=colors.HexColor("#1E293B"))
    body_bold = ParagraphStyle('BodyB', parent=body, fontName='Helvetica-Bold')
    callout_text = ParagraphStyle('Callout', parent=body, fontSize=8.5, leading=12.5, textColor=colors.HexColor("#334155"))

    story = []

    # --- EN-TÊTE DU DOCUMENT ---
    logo_path = r"c:\Users\aless\Desktop\antigravity\Alessio\projet_inov\logo.png"
    logo_flow = RLImage(logo_path, width=44, height=44) if os.path.exists(logo_path) else Paragraph("<b>PREVENT-X</b>", h2)
    
    header_info = [
        Paragraph("<b>PREVENT-X AI</b> • Le Guide Médical Ultra-Simple", h1),
        Paragraph("Comprendre le corps humain, les radios et notre IA en 10 minutes (Garanti sans jargon)", ParagraphStyle('Sub', parent=body, fontSize=9.5, textColor=colors.HexColor("#64748B")))
    ]
    hdr_table = Table([[logo_flow, header_info]], colWidths=[52, 470])
    hdr_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(hdr_table)
    story.append(HRFlowable(width="100%", thickness=2, color=c_blue, spaceAfter=10, spaceBefore=6))

    # --- INTRO : POURQUOI CE GUIDE ? ---
    intro_p = Paragraph(
        "<b>Pas besoin d'avoir fait 10 ans de médecine pour maîtriser ce projet.</b> "
        "En réalité, la mécanique du corps humain ressemble exactement à une plomberie de maison combinée à un moteur de voiture. "
        "Ce guide t'explique pas à pas ce que tu dois savoir pour comprendre ce qu'on fait et briller devant n'importe quel prof ou jury.",
        body
    )
    intro_box = Table([[intro_p]], colWidths=[522])
    intro_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(intro_box)
    story.append(Spacer(1, 10))

    # --- PARTIE 1 : COMMENT MARCHE UNE RADIO ? ---
    story.append(Paragraph("1. Comment marche une radiographie ? (La photo magique)", h2))
    p1 = Paragraph(
        "Une radio du thorax, c'est juste un appareil qui envoie des rayons invisibles (les rayons X) à travers la poitrine du patient. "
        "Derrière le patient, il y a un capteur. C'est le principe des ombres chinoises :<br/>"
        "• <b>Ce qui est vide / plein d'air (les Poumons) :</b> Les rayons traversent sans toucher d'obstacle $\\rightarrow$ Cela apparaît en <b>NOIR</b>.<br/>"
        "• <b>Ce qui est liquide / tissu mou (le Cœur et le Sang) :</b> Les rayons sont un peu freinés $\\rightarrow$ Cela apparaît en <b>GRIS</b>.<br/>"
        "• <b>Ce qui est solide et dense (les Os et le Calcium) :</b> Les rayons sont complètement bloqués $\\rightarrow$ Cela apparaît en <b>BLANC BRILLANT</b>.<br/><br/>"
        "<b>L'effet miroir (La règle de la poignée de main) :</b><br/>"
        "Quand tu regardes une radio posée devant toi, c'est comme si le patient était debout en face de toi et que tu lui serrais la main : "
        "<b>sa gauche est à ta droite</b>, et sa droite est à ta gauche ! C'est pour ça que la pointe du cœur penche vers la droite de l'écran.",
        body
    )
    story.append(p1)
    story.append(Spacer(1, 8))

    # --- IMAGE DE LA RADIO ANNOTEE ---
    annotated_img_path = r"c:\Users\aless\Desktop\antigravity\Alessio\projet_inov\assets\schema_anatomie_radio.png"
    if os.path.exists(annotated_img_path):
        radio_flow = RLImage(annotated_img_path, width=520, height=310)
        story.append(radio_flow)
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # --- PARTIE 2 : LE COEUR ET LA CRISE CARDIAQUE ---
    story.append(Paragraph("2. Le Cœur & la Crise Cardiaque (L'analogie du moteur de bagnole)", h2))
    p2 = Paragraph(
        "<b>Le cœur est une simple pompe mécanique.</b> Il se contracte 100 000 fois par jour pour pousser le sang dans tout le corps.<br/><br/>"
        "<b>Pourquoi un cœur fatigue et devient trop gros ?</b><br/>"
        "Imagine un tuyau d'arrosage bouché par un caillou : si tu veux que l'eau sorte quand même, tu dois forcer comme un malade sur la pompe. "
        "C'est exactement ça l'<b>hypertension artérielle</b> (la tension trop haute).<br/>"
        "Comme tout muscle qui force (comme à la salle de sport), le cœur commence par s'épaissir. Puis, à force de forcer pendant des années, "
        "il s'épuise, se détend comme un vieux ballon de baudruche et devient <b>trop gros</b> : c'est ce que les médecins appellent la <b>Cardiomégalie</b>.<br/><br/>"
        "<b>Ce que regarde notre IA sur la radio :</b><br/>"
        "Elle mesure la largeur du cœur et la compare à la largeur de la poitrine. C'est le <b>Rapport Cardio-Thoracique (RCT)</b> :<br/>"
        "• <b>Moins de 50% (< 0.50) :</b> Cœur de taille normale, tout va bien.<br/>"
        "• <b>Plus de 50% (> 0.50) :</b> Cœur anormalement gonflé ! Risque d'infarctus ou d'insuffisance cardiaque sévère.",
        body
    )
    story.append(p2)
    story.append(Spacer(1, 10))

    # --- PARTIE 3 : L'AORTE ET L'AVC ---
    story.append(Paragraph("3. L'Aorte & l'AVC (Le tuyau d'arrosage entartré)", h2))
    p3 = Paragraph(
        "<b>Qu'est-ce qu'un AVC (Accident Vasculaire Cérébral) ?</b><br/>"
        "C'est quand une artère dans la tête se bouche d'un coup. Le sang n'arrive plus au cerveau : en quelques secondes, des millions de neurones meurent. "
        "Le patient perd la parole ou se retrouve paralysé.<br/><br/>"
        "<b>D'où vient le bouchon ? (La Crosse Aortique) :</b><br/>"
        "L'<b>Aorte</b>, c'est l'autoroute géante qui sort du cœur. Au sommet, elle fait un virage en forme de canne (la 'crosse aortique') "
        "d'où partent les artères carotides qui montent directement alimenter le cerveau.<br/>"
        "• Quand quelqu'un fume ou mange trop gras pendant 20 ans, du cholestérol et du <b>calcaire (calcium)</b> s'incrustent sur les parois de l'aorte. "
        "C'est comme une vieille canalisation de machine à laver complètement entartrée.<br/>"
        "• Avec la pression du sang, <b>un morceau de calcaire peut se casser et s'envoler</b>. Il monte direct par la carotide et va se coincer dans le cerveau $\\rightarrow$ <b>C'est l'AVC !</b><br/><br/>"
        "<b>Ce que notre IA voit sur la radio :</b><br/>"
        "Sur une personne saine, l'aorte est invisible/grise. Mais quand elle est pleine de calcaire, elle devient <b>blanche et brillante</b> sur la radio ! "
        "Notre IA repère cette trace blanche en 1 seconde et prévient que le patient risque un AVC dans les 5 ans.",
        body
    )
    story.append(p3)
    story.append(Spacer(1, 10))

    # --- PARTIE 4 : LES OS ET L'OSTEOPOROSE ---
    story.append(Paragraph("4. Les Os & l'Ostéoporose (Les briques de Lego fragiles)", h2))
    p4 = Paragraph(
        "<b>Les os ne sont pas du plastique dur, c'est vivant.</b> Avec l'âge (surtout chez les femmes après 50 ans), les os perdent leur calcium. "
        "Ils deviennent poreux, comme un sucre trempé dans le café ou une éponge pleine de trous : c'est l'<b>Ostéoporose</b>.<br/><br/>"
        "<b>Pourquoi regarder les os sur une radio du thorax ?</b><br/>"
        "Au milieu de la poitrine, il y a la <b>colonne vertébrale</b> (les vertèbres empilées comme des briques de Lego qui portent tout ton corps).<br/>"
        "• Quand l'os devient fragile, une vertèbre ne résiste plus au poids du corps et s'écrase sur elle-même : c'est un <b>tassement vertébral</b>.<br/>"
        "• Le patient a souvent juste 'un peu mal au dos' sans savoir que sa vertèbre s'est aplatie.<br/>"
        "• <b>Le piège mortel :</b> Quelqu'un qui a une vertèbre tassée a <b>5 fois plus de risques</b> de se casser le col du fémur (la hanche) à la première petite chute.<br/><br/>"
        "<b>Ce que notre IA fait :</b><br/>"
        "Pendant que le médecin regarde les poumons, l'IA inspecte la colonne en arrière-plan. Si elle voit que les vertèbres sont trop sombres (perte de densité) "
        "ou qu'une vertèbre a perdu de la hauteur, elle alerte immédiatement.",
        body
    )
    story.append(p4)
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # --- PARTIE 5 : POURQUOI PREVENT-X EST UN COUP DE GENIE ---
    story.append(Paragraph("5. Pourquoi PREVENT-X AI est un coup de génie médical ?", h2))
    p5 = Paragraph(
        "Aujourd'hui dans le monde réel :<br/>"
        "1. Un médecin généraliste n'a que 15 minutes par patient. Il tape l'âge et la tension dans un formulaire statistique théorique (SCORE2), "
        "mais il ne sait pas ce qui se passe VRAIMENT à l'intérieur du corps de son patient.<br/>"
        "2. Un radiologue qui reçoit la radio regarde juste si le patient a une pneumonie ou une fracture de côte, puis passe au suivant. "
        "Il n'a pas le temps de mesurer l'aorte au millimètre ni de vérifier la hauteur de chaque vertèbre.<br/><br/>"
        "<b>Ce que fait PREVENT-X AI :</b><br/>"
        "Notre IA prend la radio de routine que le patient a faite pour une toux, la croise avec sa tension et son âge, et délivre en <b>2 secondes</b> :<br/>"
        "• Le risque réel d'infarctus et d'AVC à 5 ans.<br/>"
        "• Une <b>carte colorée (Grad-CAM)</b> qui montre au médecin exactement où regarder en rouge sur l'aorte ou le cœur.<br/>"
        "• Un compte-rendu PDF officiel prêt à imprimer pour sauver la vie du patient avant qu'il ne fasse son accident.",
        body
    )
    story.append(p5)
    story.append(Spacer(1, 12))

    # --- TABLEAU RECAPITULATIF : LES 5 MOTS COMPLIQUES TRADUITS EN FRANCAIS SIMPLE ---
    story.append(Paragraph("6. Lexique de survie pour briller devant les profs de l'EPSI", h2))
    
    lexique_data = [
        [Paragraph("<b>Mot Médical Savant</b>", body_bold), Paragraph("<b>Ce que ça veut dire en vrai (Langage simple)</b>", body_bold)],
        [
            Paragraph("<b>Cardiomégalie</b>", body),
            Paragraph("Le cœur est trop gros / dilaté parce qu'il a forcé pendant des années contre une tension trop haute.", body)
        ],
        [
            Paragraph("<b>Rapport Cardio-Thoracique (RCT)</b>", body),
            Paragraph("La largeur du cœur divisée par la largeur de la poitrine. Si le cœur fait plus de 50% de la largeur, c'est anormal.", body)
        ],
        [
            Paragraph("<b>Crosse Aortique Calcifiée</b>", body),
            Paragraph("Le tuyau principal qui alimente le cerveau est plein de calcaire (tartre). Risque majeur qu'un bout s'arrache et cause un AVC.", body)
        ],
        [
            Paragraph("<b>Ostéopénie / Tassement</b>", body),
            Paragraph("Les os deviennent comme des éponges et une vertèbre s'écrase sur elle-même. Signe avant-coureur de fracture grave.", body)
        ],
        [
            Paragraph("<b>Heatmap Grad-CAM</b>", body),
            Paragraph("La carte de chaleur colorée (rouge/jaune) qui prouve au médecin quelle zone de l'image a fait sonner l'alarme de l'IA.", body)
        ],
        [
            Paragraph("<b>Fusion Multimodale</b>", body),
            Paragraph("Croiser deux sources différentes : les chiffres du formulaire (tension/âge) + les pixels de la radio dans le même calcul.", body)
        ]
    ]

    lex_table = Table(lexique_data, colWidths=[180, 342])
    lex_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(lex_table)

    # Build PDF
    doc.build(story)
    print("Beginner guide PDF successfully built at:", output_pdf_path)

if __name__ == "__main__":
    out_pdf = r"c:\Users\aless\Desktop\antigravity\Alessio\projet_inov\docs\GUIDE_MEDECINE_POUR_DEBUTANT.pdf"
    build_pdf(out_pdf)
