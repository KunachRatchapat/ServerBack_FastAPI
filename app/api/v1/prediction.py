from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.response import success_response
from app.ml.service import ml_service

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("/")
async def predict(file: UploadFile = File(...)):
    if not ml_service.ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI models are not loaded",
        )
    try:
        result = ml_service.predict(file)
        return success_response(result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
