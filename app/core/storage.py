import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from PIL import Image

from app.config import settings
from app.core.logging_conf import logger

ALLOWED_EXTENSIONS = settings.allowed_extensions_set
MAX_FILE_SIZE = settings.MAX_UPLOAD_SIZE
THUMBNAIL_SIZE = settings.thumbnail_size
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
        logger.warning("Failed to create thumbnail for %s", filepath.name)


def get_file_path(filename: str) -> Path:
    if not filename or Path(filename).name != filename:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")

    upload_root = UPLOAD_DIR.resolve()
    full = (upload_root / filename).resolve()
    try:
        full.relative_to(upload_root)
    except ValueError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")

    if not full.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="File not found")
    return full
