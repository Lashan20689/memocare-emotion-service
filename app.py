from fastapi import FastAPI, UploadFile, File
from deepface import DeepFace
import shutil
import os

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/detect-emotion")
async def detect_emotion(file: UploadFile = File(...)):
    temp_path = "temp_frame.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = DeepFace.analyze(
            img_path=temp_path,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='mtcnn'
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    if not result:
        return {"success": False, "message": "No face detected"}

    emotions = result[0]['emotion']
    dominant = result[0]['dominant_emotion']

    return {
        "success": True,
        "dominantEmotion": dominant,
        "emotionScores": {k: round(float(v), 2) for k, v in emotions.items()},
    }
