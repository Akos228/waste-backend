# main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import numpy as np
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("yolov8n.pt")

CATEGORIES = {
    "bottle": "plastic",
    "banana": "organique",
    "book": "papier",
    "can": "métal",
    "syringe": "dangereux",
    "battery": "dangereux",
}

DANGEROSITY = {
    "plastic": "faible",
    "organique": "faible",
    "papier": "faible",
    "métal": "modérée",
    "dangereux": "élevée"
}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = model.predict(np.array(image))

    for box in results[0].boxes:
        class_id = int(box.cls[0])
        label = model.names[class_id]
        confidence = float(box.conf[0])

        category = CATEGORIES.get(label, "non classé")
        danger = DANGEROSITY.get(category, "inconnue")

        return {
            "objet": label,
            "categorie": category,
            "dangerosite": danger,
            "confiance": round(confidence, 2)
        }

    return {
        "objet": "inconnu",
        "categorie": "non classé",
        "dangerosite": "inconnue",
        "confiance": 0
    }
