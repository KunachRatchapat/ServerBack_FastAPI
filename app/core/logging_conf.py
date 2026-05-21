import logging
import sys
from time import perf_counter

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


def setup_logging() -> None:
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-5s %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)

    for name in ("uvicorn.access", "uvicorn.error", "alembic"):
        logging.getLogger(name).setLevel(logging.WARNING)


logger = logging.getLogger("serverback")


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start = perf_counter()
        response = await call_next(request)
        duration_ms = int((perf_counter() - start) * 1000)

        method = request.method
        path = request.url.path
        qs = request.url.query
        status = response.status_code
        ip = request.client.host if request.client else "?"

        qs_part = f"?{qs}" if qs else ""
        logger.info(
            "%s %s%s -> %s [%dms] %s",
            method, path, qs_part, status, duration_ms, ip,
        )
        return response
