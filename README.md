# ServerBack FastAPI

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![License](https://img.shields.io/badge/license-MIT-green)

> Final-year project backend — Fruit & vegetable image classification API  
> Built with **FastAPI** + **PyTorch (Img2Vec)** + **scikit-learn (Random Forest)**

---

## 📌 About

This API lets you:

- **Classify** fruit & vegetable images using AI (Img2Vec feature extraction + Random Forest)
- **Browse** a catalog of fruits and vegetables with nutrition info
- **Search** by name across the entire catalog
- **Authenticate** via JWT (register, login, email verification, forgot/reset password)
- **Manage favorites** — users can save their preferred items
- **Administer** users and view dashboard stats

All entities use **soft delete** — data is never permanently removed.

---

## ✨ Features

| Category | Details |
|----------|---------|
| **Image AI** | Upload → classify via Img2Vec + Random Forest |
| **Auth** | JWT (15m access + 7d refresh), Argon2 hashing, email verification |
| **Domains** | Fruits, Vegetables, Nutrition, Favorites, Search, Auth, Admin |
| **Search** | ILIKE name search across fruits & vegetables |
| **Nutrition** | CRUD + lookup by fruit/vegetable |
| **Soft Delete** | All entities — `deleteat` timestamp, auto-filtered from queries |
| **Pagination** | All list endpoints with HATEOAS-style next/previous URLs |
| **Rate Limiter** | 60 req/min (production only) |
| **Auto Migration** | Alembic runs on startup — zero manual migration steps |
| **File Upload** | Image upload with thumbnail generation (max 5MB) |
| **Response Envelope** | Consistent `{ code, status, message, result }` format |
| **Custom Exceptions** | `NotFoundError`, `ConflictError`, `BadRequestError`, etc. |
| **Docs** | Interactive Swagger UI at `/docs` |

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/KunachRatchapat/ServerBack_FastAPI.git
cd ServerBack_FastAPI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start dev server (SQLite — zero config)
uvicorn app.main:app --reload
```

Open **http://localhost:8000/docs** for interactive API docs.

### Docker

```bash
docker build -t serverback-fastapi .
docker run -p 8000:8000 serverback-fastapi
```

---

## 📖 API Overview

All endpoints live under `/api/v1`:

| Router | Prefix | Auth | Description |
|--------|--------|------|-------------|
| Auth | `/auth` | Mixed | Register, login, refresh, verify email, forgot/reset password, profile |
| Fruits | `/fruits` | Admin write | List, get, create, update, delete fruits |
| Vegetables | `/vegetables` | Admin write | List, get, create, update, delete vegetables |
| Nutrition | `/nutrition` | Admin write | CRUD nutrition info + lookup by fruit/vegetable |
| Favorites | `/favorites` | User | Toggle & list user's favorites |
| Search | `/search` | Public | Search fruits & vegetables by name |
| Admin | `/admin` | Admin only | User management + dashboard stats |
| Predict | `/predict` | Public | Upload image → AI classification |
| Upload | `/upload` | User upload | File upload + public file serving |
| — | `/health` | Public | Health check (DB + ML status) |

See full interactive docs at **`/docs`**.

---

## 🏗️ Project Structure

```
ServerBack_FastAPI/
├── app/
│   ├── main.py                  # Entry point (middleware, lifespan, exception handlers)
│   ├── config.py                # Pydantic-settings (DB, JWT, ML, etc.)
│   ├── api/v1/                  # 9 routers (auth, fruits, vegetables, nutrition, ...)
│   ├── core/                    # Shared: repository, response, security, exceptions, etc.
│   ├── domains/                 # 7 domains: auth, fruit, vegetable, nutrition, favorite, admin, search
│   ├── database/                # Engine, session, Alembic migrations
│   └── ml/                      # AI model loading + prediction
├── db/models/                   # SQLModel table definitions (User, Fruit, Vegetable, ...)
├── tests/                       # 69 tests across 10 files
├── ai_model/                    # ML model pickle + label files
├── uploads/                     # Uploaded images + thumbnails
├── Dockerfile
├── requirements.txt
└── README.md
```

### Architecture Flow

```
Router (api/v1/) → Service (domains/*/service.py) → Repository (domains/*/repository.py) → DB
```

Each domain follows the same pattern: `schemas.py` (Pydantic) → `service.py` (logic) → `repository.py` (CRUD).

---

## ⚙️ Environment Variables

Create a `.env` file in the project root (all optional in dev):

| Variable | Default | Description |
|----------|---------|-------------|
| `ENV` | `development` | Set to `production` to enable rate limiter |
| `DATABASE_URL` | `sqlite:///./dev.db` | PostgreSQL for production |
| `SECRET_KEY` | `""` | JWT signing key (**required in production**) |
| `CORS_ORIGINS` | `http://localhost:8000` | Comma-separated allowed origins |
| `UPLOAD_DIR` | `uploads` | Directory for uploaded files |

---

## 🧪 Testing & Linting

```bash
# Run all tests (69 tests)
pytest tests/ -v

# Single file
pytest tests/test_auth.py -v

# Lint
ruff check app/ tests/

# Type check
mypy app/ tests/ --explicit-package-bases
```

**Pre-commit order:** `ruff` → `mypy` → `pytest`

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| Framework | FastAPI (Python 3.12) |
| Database | PostgreSQL (prod) / SQLite (dev) |
| ORM | SQLModel + SQLAlchemy + Alembic |
| Auth | JWT (python-jose) + Argon2 (passlib) |
| ML | PyTorch (Img2Vec) + scikit-learn (Random Forest) |
| Validation | Pydantic v2 |
| Dev Tools | Ruff (lint), Mypy (type check), Pytest (test) |
| Container | Docker |

---

## 📄 License

MIT
