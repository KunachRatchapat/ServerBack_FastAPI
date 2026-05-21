import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from PIL import Image

from app.config import settings

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024
THUMBNAIL_SIZE = (300, 300)
UPLOAD_DIR = Path(settings.UPLOAD_DIR)


def ensure_upload_dir():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def validate_image(file: UploadFile) -> None:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {ext}. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    content = file.file.read()
    file.file.seek(0)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large ({len(content)} bytes). Max: {MAX_FILE_SIZE} bytes",
        )


async def save_upload(file: UploadFile) -> str:
    ensure_upload_dir()
    validate_image(file)

    ext = Path(file.filename or "").suffix.lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = UPLOAD_DIR / filename

    content = await file.read()
    filepath.write_bytes(content)

    create_thumbnail(filepath)

    return filename


def create_thumbnail(filepath: Path) -> None:
    thumb_dir = UPLOAD_DIR / "thumbnails"
    thumb_dir.mkdir(parents=True, exist_ok=True)
    thumb_path = thumb_dir / filepath.name

    try:
        img = Image.open(filepath)
        img.thumbnail(THUMBNAIL_SIZE)
        img.save(thumb_path)
    except Exception:
        pass


def get_file_path(filename: str) -> Path:
    full = UPLOAD_DIR / filename
    if not full.exists() or not full.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")
    return full
