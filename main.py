import warnings
warnings.warn(
    "main.py is deprecated — use 'uvicorn app.main:app' instead",
    DeprecationWarning,
    stacklevel=2,
)

from app.main import app
