# ServerBack FastAPI — Agent Guide

## Commands
```bash
uvicorn app.main:app --reload              # dev server
python -m pytest tests/ -v                # all tests (47 tests)
python -m pytest tests/test_auth.py -v    # single file
python -m ruff check app/ tests/          # lint
python -m mypy app/ tests/ --explicit-package-bases  # typecheck
python -m alembic upgrade head            # apply latest migration
python -m alembic revision --autogenerate -m "message"  # new migration
```

**Pre-commit order:** `ruff -> mypy -> pytest`

## Architecture

- **Domain pattern:** Each domain has `schemas.py` (pydantic) → `service.py` (business logic) → `repository.py` (SQLModel CRUD). Services hard-code their repo (no DI).
- **Response envelope:** All endpoints return `{"code", "status", "message", "result"}` via `success_response()` / `created_response()` — never return raw models directly.
- **Soft delete:** All models have `deleteat`/`createat`/`updateat` (lowercase, no underscores). `SQLModelRepository` auto-filters `WHERE deleteat IS NULL` on get/list, auto-sets `updateat` on update, and sets `deleteat` on delete (not hard delete).
- **Auth:** JWT (15m access + 7d refresh), Argon2 password hashing via passlib. New users start with `is_verified=False` — login returns 403 until email verified.

## Project Structure
```
app/main.py          # entry point (lifespan auto-migrates DB + loads ML)
app/config.py        # pydantic-settings; SQLite in dev, Postgres in prod
app/api/v1/          # 9 routers: fruits, vegetables, auth, admin, favorites, nutrition, prediction, search, upload
app/core/            # shared: repository, response, security, storage, rate_limit, pagination, logging
app/domains/         # 6 domains: auth, fruit, vegetable, favorite, admin, nutrition
db/models/           # SQLModel tables: user, fruit, vegetable, favorite, nutrition
tests/               # 47 tests in 9 files, file-based SQLite (test.db)
```

## Gotchas

- **Terminal is cp874** — use only ASCII-safe characters in logs (`->` not `→`). `print()` with non-ASCII chars will crash on this machine.
- **`img2vec_pytorch` is not installed** — ML endpoints return 503. The Random Forest pickle file is also missing from the repo.
- **Auto-migration on startup** — Alembic runs `upgrade head` in `lifespan` before the app serves requests. Destructive migrations run automatically.
- **Rate limiter** (slowapi, 60/min) only active when `ENV=production`.
- **Argon2 is slow** — tests that seed users will run slower than usual.
- **`SECRET_KEY` must be set in production** — default in `config.py` is empty. JWT signing will fail without it.

## Legacy code (do not modify)
- `repository/` — old repo pattern
- `db/database.py` — deprecated, re-exports `app.database.engine`
- `main.py` (root) — deprecated, re-exports `app.main`
