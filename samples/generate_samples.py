import cv2
import numpy as np
from pathlib import Path

def generate_chest_xray(case_type="normal"):
    """
    Génère une radiographie thoracique réaliste avec les repères anatomiques :
    - Poumons (radiotransparents / sombres)
    - Silhouette cardiaque (radio-opaque / claire)
    - Crosse aortique & médiastin
    - Gril costal & colonne vertébrale
    """
    h, w = 640, 640
    img = np.zeros((h, w), dtype=np.uint8) + 25  # Fond sombre tissu mou
    
    # 1. Cage thoracique générale (ellipse osseuse externe)
    cv2.ellipse(img, (320, 360), (250, 290), 0, 0, 360, 45, -1)
    
    # 2. Champs pulmonaires (deux lobes sombres)
    # Poumon droit (à gauche sur la radio)
    cv2.ellipse(img, (220, 310), (95, 180), -8, 0, 360, 15, -1)
    # Poumon gauche (à droite sur la radio)
    cv2.ellipse(img, (420, 310), (95, 180), 8, 0, 360, 15, -1)

    # 3. Silhouette Cardiaque (au centre/gauche)
    # Variation selon le cas
    cardio_size = (85, 110) if case_type != "cardiomegaly" else (125, 140)
    cardio_center = (360, 390) if case_type != "cardiomegaly" else (375, 400)
    cv2.ellipse(img, cardio_center, cardio_size, 25, 0, 360, 160, -1)

    # 4. Crosse Aortique (Bouton aortique à x=365, y=260)
    aorta_brightness = 190 if case_type == "aortic_calcification" else 140
    cv2.circle(img, (365, 260), 28, aorta_brightness, -1)
    if case_type == "aortic_calcification":
        # Calcification dense visible sur la paroi de la crosse
        cv2.ellipse(img, (365, 258), (26, 12), -20, 10, 160, 245, 3)

    # 5. Rachis thoracique (colonne au centre)
    spine_brightness = 90 if case_type == "osteopenia" else 135
    for y in range(120, 560, 24):
        cv2.rectangle(img, (308, y), (332, y + 16), spine_brightness, -1)
        if case_type == "osteopenia" and y in [312, 336]:
            # Micro-tassement vertébral (hauteur réduite)
            cv2.rectangle(img, (308, y), (332, y + 8), 170, -1)

    # 6. Côtes (arcs costaux bilatéraux)
    for r in range(160, 520, 40):
        cv2.ellipse(img, (320, r), (220, 85), 0, 20, 160, 80, 5)

    # 7. Diaphragmes et culs-de-sac pleuraux
    cv2.ellipse(img, (200, 480), (130, 70), 0, 180, 360, 175, -1)
    cv2.ellipse(img, (440, 490), (130, 70), 0, 180, 360, 175, -1)

    # 8. Clavicules
    cv2.line(img, (160, 150), (300, 175), 160, 8)
    cv2.line(img, (480, 150), (340, 175), 160, 8)

    # 9. Flou gaussien pour aspect radiologique continu + léger bruit scanner
    img = cv2.GaussianBlur(img, (21, 21), 0)
    noise = np.random.normal(0, 4, (h, w)).astype(np.int16)
    noisy_img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Anonymisation médicale : Tag d'orientation
    cv2.putText(noisy_img, "R", (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, 180, 2)
    cv2.putText(noisy_img, "PREVENT-X ANONYMIZED", (40, 610), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 90, 1)

    return noisy_img

if __name__ == "__main__":
    out_dir = Path(r"c:\Users\aless\Desktop\antigravity\Alessio\projet_inov\samples")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    cv2.imwrite(str(out_dir / "sample_case1_aortic.png"), generate_chest_xray("aortic_calcification"))
    cv2.imwrite(str(out_dir / "sample_case2_normal.png"), generate_chest_xray("normal"))
    cv2.imwrite(str(out_dir / "sample_case3_cardiomegaly_bone.png"), generate_chest_xray("cardiomegaly"))
    cv2.imwrite(str(out_dir / "sample_case3_osteopenia.png"), generate_chest_xray("osteopenia"))
    print("Sample X-ray images generated successfully!")
