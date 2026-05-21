from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text

from app.api.v1.router import v1_router
from app.config import settings
from app.core.exceptions import global_exception_handler
from app.core.logging_conf import RequestLogMiddleware, setup_logging
from app.core.rate_limit import limiter
from app.core.security_headers import SecurityHeadersMiddleware
from app.database.engine import engine
from app.ml.service import ml_service


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("script_location", "app/database/migrations")
    command.upgrade(alembic_cfg, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    ml_service.load()
    yield


setup_logging()

app = FastAPI(
    title="ServerBack FastAPI",
    version="1.2.0",
    lifespan=lifespan,
)

app.state.limiter = limiter


def rate_limit_handler(request: Request, exc: Exception) -> Response:
    return _rate_limit_exceeded_handler(request, exc)  # type: ignore[arg-type]


app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLogMiddleware)

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(v1_router)


@app.get("/health")
def health():
    db_ok = False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_ok = True
    except Exception:
        db_ok = False
    return {
        "status": "ok" if db_ok else "degraded",
        "env": settings.ENV,
        "database": "connected" if db_ok else "disconnected",
        "ml_model": "loaded" if ml_service.ready else "not_loaded",
    }
