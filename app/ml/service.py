import io
import os
import pickle
from typing import Any

from fastapi import UploadFile
from PIL import Image

MODEL_PATH = "ai_model/my_food_classifier_rf.pkl"
LABELS_PATH = "ai_model/my_food_classifier_labels.txt"


class MLService:
    def __init__(self) -> None:
        self._rf_model: Any = None
        self._img2vec_model: Any = None
        self._class_names: list[str] = []
        self._loaded = False

    def load(self) -> None:
        try:
            from img2vec_pytorch import Img2Vec

            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
            with open(MODEL_PATH, "rb") as f:
                self._rf_model = pickle.load(f)

            self._img2vec_model = Img2Vec(cuda=False)

            if not os.path.exists(LABELS_PATH):
                raise FileNotFoundError(f"Labels not found: {LABELS_PATH}")
            with open(LABELS_PATH, "r", encoding="utf-8") as f:
                self._class_names = [line.strip() for line in f.readlines()]

            self._loaded = True
            print(f"ML models loaded. Classes: {self._class_names}")
        except Exception as e:
            print(f"ML models NOT loaded ({e}) — /predict will return 503")

    @property
    def ready(self) -> bool:
        return self._loaded

    def predict(self, file: UploadFile) -> dict:
        if not self._loaded:
            raise RuntimeError("ML models not loaded")

        contents = file.file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        features = self._img2vec_model.get_vec(img)

        prediction_array = self._rf_model.predict([features])
        probabilities = self._rf_model.predict_proba([features])[0]
        predicted_class = prediction_array[0]
        class_indices = list(self._rf_model.classes_)

        if predicted_class in class_indices:
            index = class_indices.index(predicted_class)
            confidence = float(probabilities[index])
        else:
            confidence = 0.0

        return {"class": str(predicted_class), "confidence": confidence}


ml_service = MLService()
