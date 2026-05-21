import warnings
warnings.warn(
    "db/database.py is deprecated — use app.database.engine instead",
    DeprecationWarning,
    stacklevel=2,
)

from app.database.engine import engine, get_session

__all__ = ["engine", "get_session"]
