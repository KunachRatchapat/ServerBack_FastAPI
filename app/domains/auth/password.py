import re

from fastapi import HTTPException, status

MIN_LENGTH = 8
MAX_LENGTH = 128


def validate_password(password: str) -> None:
    if len(password) < MIN_LENGTH:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Password must be at least {MIN_LENGTH} characters",
        )
    if len(password) > MAX_LENGTH:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Password must be at most {MAX_LENGTH} characters",
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least one uppercase letter",
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least one lowercase letter",
        )
    if not re.search(r"\d", password):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least one digit",
        )
