import warnings

warnings.warn(
    "repository/jwt.py is deprecated — use app.core.security instead",
    DeprecationWarning,
    stacklevel=2,
)

from app.core.security import create_token as generate_token
from app.core.security import decode_token

SECRET_KEY = None
ALGORITHM = None
ACCESS_TOKEN_EXPIRE_MINUTES = None


class JWTRepo:
    generate_token = staticmethod(generate_token)
    decode_token = staticmethod(decode_token)
