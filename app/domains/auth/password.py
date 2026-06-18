import re

from app.config import settings
from app.core.exceptions import ValidationError

MIN_LENGTH = settings.PASSWORD_MIN_LENGTH
MAX_LENGTH = settings.PASSWORD_MAX_LENGTH


def validate_password(password: str) -> None:
    if len(password) < MIN_LENGTH:
        raise ValidationError(
            f"Password must be at least {MIN_LENGTH} characters",
        )
    if len(password) > MAX_LENGTH:
        raise ValidationError(
            f"Password must be at most {MAX_LENGTH} characters",
        )
    if not re.search(r"[A-Z]", password):
        raise ValidationError(
            "Password must contain at least one uppercase letter",
        )
    if not re.search(r"[a-z]", password):
        raise ValidationError(
            "Password must contain at least one lowercase letter",
        )
    if not re.search(r"\d", password):
        raise ValidationError(
            "Password must contain at least one digit",
        )
