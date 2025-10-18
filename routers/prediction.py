from fastapi import APIRouter, File, UploadFile, HTTPException, status
import os
import io
import pickle
from PIL import Image
from img2vec_pytorch import Img2Vec


router = APIRouter()
rf_model =None
img2vec_model = None
class_name = []

MODEL_PATH = 'ai_model/my_food_classifier_rf.pkl'
LABELS_PATH = 'ai_model/my_food_classifier_labels.txt'

@router.on_event("startup")
async def load_models_on_startup():
    global rf_model, img2vec_model, class_names
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Random Forest Model file not found at:{MODEL_PATH}")
        with open(MODEL_PATH,'rb') as f:
            rf_model = pickle.load(f)
            
        img2vec_model = Img2Vec(cuda=False)
        
        
        # --- โหลด Class Names (Labels) ---
        if not os.path.exists(LABELS_PATH):
            raise FileNotFoundError(f"Labels Filde not found at:{LABELS_PATH}") 
        with open(LABELS_PATH,'r',encoding='utf-8') as f:
            
            class_names = [line.strip() for line in f.readlines()]
            
        print("AI models (Random Forest, Img2Vec) and labels loaded successfully! ") 
        print(f"Detected classes: {class_names}")
        
    except Exception as e:
        print(f"Error loading models on startup:{e}")
        
        raise RuntimeError(f"Failed to load AI models on startup:{e}")
    
@router.post("/predict")
async def predict_image(file: UploadFile =  File(...)):
    if rf_model is None or img2vec_model is None or not class_names:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="AI models are not ready. Server failed to load resources.!")
    
    contents = await file.read() 
    
    try:
        img = Image.open(io.BytesIO(contents)).convert('RGB')
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file format")
    
    features = img2vec_model.get_vec(img)
    
    prediction_array = rf_model.predict([features])
    probabilities = rf_model.predict_proba([features])[0]
    
    predicted_class_name = prediction_array[0]
    
    class_indices = list(rf_model.classes_)
    
    if predicted_class_name in class_indices:
        index = class_indices.index(predicted_class_name)
        confidence_score = probabilities[index]
    else:
        confidence_score = 0.0
        
    return {
        "class": str(predicted_class_name),
        "confidence" : float(confidence_score)
    }
