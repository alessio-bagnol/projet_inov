"""
samples/create_sample_dicom.py
Génère un véritable fichier DICOM (.dcm) conforme aux standards ACR/NEMA & DICOM 3.0
avec les tags d'un examen radiologique thoracique anonymisé.
"""

import time
import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, SecondaryCaptureImageStorage, generate_uid
from PIL import Image

def create_dicom(input_png_path: str, output_dcm_path: str):
    # Charger l'image radiologique en niveaux de gris
    pil_img = Image.open(input_png_path).convert('L')
    img_data = np.array(pil_img, dtype=np.uint8)

    # Métadonnées du fichier (Part 10 Header)
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    file_meta.ImplementationClassUID = generate_uid()

    # Création du dataset DICOM
    ds = FileDataset(output_dcm_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Tags d'anonymisation et de modalité clinique
    ds.Modality = "CR"  # Computed Radiography
    ds.SeriesDescription = "CHEST PA PREVENT-X CLINICAL SCAN"
    ds.BodyPartExamined = "CHEST"
    ds.PatientPosition = "PA"
    
    # Anonymisation RGPD stricte
    ds.PatientName = "ANONYMIZED^PATIENT"
    ds.PatientID = "PX-2026-9021"
    ds.PatientBirthDate = "19650101"
    ds.PatientSex = "M"
    ds.PatientAge = "061Y"
    
    # Dates d'examen
    ds.StudyDate = time.strftime("%Y%m%d")
    ds.StudyTime = time.strftime("%H%M%S")
    ds.AccessionNumber = "ACC-2026-4412"
    ds.StudyID = "ST-9921"
    
    # Données d'échantillonnage de pixels
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.Rows = img_data.shape[0]
    ds.Columns = img_data.shape[1]
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelData = img_data.tobytes()

    # UIDs requis
    ds.SOPClassUID = SecondaryCaptureImageStorage
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()

    # Sauvegarde
    ds.save_as(output_dcm_path, write_like_original=False)
    print(f"DICOM file successfully created: {output_dcm_path}")

if __name__ == "__main__":
    create_dicom(
        r"c:\Users\aless\Desktop\antigravity\Alessio\projet_inov\samples\sample_case1_aortic.png",
        r"c:\Users\aless\Desktop\antigravity\Alessio\projet_inov\samples\sample_patient_cxr.dcm"
    )
