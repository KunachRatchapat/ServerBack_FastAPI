from fastapi import APIRouter, File, UploadFile, HTTPException, status
from typing import List
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import io
import keras

router = APIRouter()

try:
    model = keras.models.load_model('ai_model/keras_model.h5', compile=False)
    class_names = open('ai_model/labels.txt', 'r', encoding='utf-8').readlines()  # อ่านโมเดลทุกตัวทุกบรรทัด
except Exception as e:
    model = None
    class_names = []

@router.post("/predict")
async def predict_images(file: UploadFile = File(...)):
    if model is None or not class_names:
        raise HTTPException(status_code=500, detail="Model or class labels not loaded.")

    #-- อ่านไฟล์รูปภาพ --
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')

    #-- ปรับขนาดรูปให้ตรงกับโมเดล --
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.array(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    #-- เตรียมข้อมูล --
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    #-- Predict --
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()[2:] if len(class_names) > index else "Unknown"
    confidence_score = prediction[0][index]

    return {
        "class": class_name,
        "confidence": float(confidence_score)
    }
    
    
    
    