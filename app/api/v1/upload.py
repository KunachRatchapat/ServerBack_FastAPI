from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from app.api.deps import CurrentUserDep
from app.core.response import success_response
from app.core.storage import get_file_path, save_upload

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload_file(current_user: CurrentUserDep, file: UploadFile = File(...)):
    filename = await save_upload(file)
    return success_response({"filename": filename}, "Upload successful")


@router.get("/{filename}")
def get_file(filename: str):
    filepath = get_file_path(filename)
    return FileResponse(filepath)
