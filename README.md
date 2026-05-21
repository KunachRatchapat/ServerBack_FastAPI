# ServerBack FastAPI

> Final-year project backend — fruit & vegetable classification API
> built with FastAPI + Img2Vec + Random Forest

## Features

- Image upload -> classification via Img2Vec feature extraction + Random Forest
- 6 domains: fruits, vegetables, nutrition, favorites, auth, admin
- JWT auth (15m access + 7d refresh) with email verification flow
- Forgot / reset password
- Soft delete on all entities
- Paginated list endpoints
- Rate limiter (production only)
- Nutrition info CRUD + lookup by fruit/vegetable
- Swagger docs at `/docs`

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs

## Tech Stack

FastAPI · SQLModel · Alembic · Pydantic · JWT (jose) · Argon2 (passlib) ·
Img2Vec (PyTorch) · scikit-learn · PostgreSQL (dev: SQLite) · Docker

## Test / Lint / Typecheck

```bash
python -m pytest tests/ -v            # 47 tests
python -m ruff check app/ tests/      # lint
python -m mypy app/ --explicit-package-bases  # typecheck
```
