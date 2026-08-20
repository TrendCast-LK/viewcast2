# ViewCast — Backend

FastAPI backend for ViewCast: auth, user accounts, and predictions. The
actual ML model is **not** wired in yet — `app/services/prediction_engine.py`
returns a deterministic mock forecast so the rest of the stack has real data
to work with. See the big comment at the top of that file for where the real
model call goes.

## Stack

- FastAPI + Uvicorn
- SQLAlchemy 2.0 (SQLite by default, swappable via `DATABASE_URL`)
- JWT auth (PyJWT + bcrypt password hashing)
- Local file storage for thumbnail/dataset uploads, served from `/uploads`

## Getting started

Requires Python 3.11 or 3.12 (Python 3.14 currently lacks prebuilt wheels for
some dependencies — if `pip install` tries to compile from source, use 3.12
instead).

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # edit SECRET_KEY etc. as needed

uvicorn app.main:app --reload --port 8000
```

The API is then at http://localhost:8000, with interactive docs at
http://localhost:8000/docs.

Tables are created automatically on startup (no migrations yet — fine for a
scaffold, swap in Alembic once the schema needs to evolve carefully).

## Endpoints

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| POST | `/auth/signup` | – | Create an account, returns a token + user |
| POST | `/auth/login` | – | OAuth2 form login (`username` = email), returns a token + user |
| GET | `/auth/me` | ✓ | Current user's profile |
| GET | `/dashboard/summary` | ✓ | Name, subscriber/view stats, prediction count |
| POST | `/predictions` | ✓ | Create a prediction (multipart form — see below) |
| GET | `/predictions` | ✓ | List the current user's predictions |
| GET | `/predictions/{id}` | ✓ | Full prediction detail incl. forecast trajectory |
| DELETE | `/predictions/{id}` | ✓ | Delete a prediction |
| GET | `/health` | – | Liveness check |

`POST /predictions` is a multipart form matching the "New Prediction" screen:
`title`, `category`, `tags` (comma-separated string), `target_date`,
`target_time`, `save_as_draft` (bool), `thumbnail` (file), `dataset` (file).
When `save_as_draft` is false, a forecast is generated immediately and
returned in the response (`predicted_views`, `confidence`, `change_vs_avg`,
`trajectory`).

Authenticated requests send `Authorization: Bearer <access_token>`.

## Project layout

```
app/
  main.py             FastAPI app, CORS, static /uploads mount, router wiring
  config.py           Settings (reads .env)
  database.py         SQLAlchemy engine/session
  models.py           User, Prediction ORM models
  schemas.py          Pydantic request/response models
  auth.py             Password hashing, JWT issue/verify, get_current_user
  routers/
    auth.py           /auth/*
    dashboard.py      /dashboard/*
    predictions.py    /predictions/*
  services/
    prediction_engine.py   Mock forecast generator — TODO: real model here
  utils/
    files.py          Upload handling (size limits, unique filenames)
```

## Connecting the frontend

The frontend (`../frontend`) is currently client-side only — its Sign In /
Sign Up / New Prediction flows just navigate between screens without calling
an API. Wiring it up to this backend (replace `navigate(...)` calls with
`fetch`/`axios` calls to the endpoints above, store the JWT, etc.) hasn't
been done yet.
