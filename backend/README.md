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
| PATCH | `/auth/me` | ✓ | Update `full_name` / `subscribers` / `monthly_views` |
| POST | `/auth/change-password` | ✓ | Change password (`current_password`, `new_password`) |
| GET | `/dashboard/summary` | ✓ | Name, subscriber/view stats, prediction count |
| POST | `/predictions` | ✓ | Create a prediction (multipart form — see below) |
| GET | `/predictions` | ✓ | List the current user's predictions |
| GET | `/predictions/{id}` | ✓ | Full prediction detail incl. forecast trajectory |
| DELETE | `/predictions/{id}` | ✓ | Delete a prediction |
| GET | `/trends/summary` | ✓ | Aggregates across the user's predictions — totals, average views/confidence, best category, per-category breakdown, and a timeline for charting |
| GET | `/channel/me` | ✓ | The user's fetched YouTube channel data |
| POST | `/channel/refresh` | ✓ | Re-fetch the channel from YouTube (retry after a failure, or pull fresh stats) |
| GET | `/notifications` | ✓ | The user's notifications (newest first, max 50) + unread count |
| POST | `/notifications/{id}/read` | ✓ | Mark one notification read |
| POST | `/notifications/read-all` | ✓ | Mark all notifications read |
| GET | `/health` | – | Liveness check |

`POST /predictions` is a multipart form matching the "New Prediction" screen:
`title`, `category`, `tags` (comma-separated string), `target_date`,
`target_time`, `save_as_draft` (bool), `thumbnail` (file), `dataset` (file).
When `save_as_draft` is false, a forecast is generated immediately and
returned in the response (`predicted_views`, `confidence`, `change_vs_avg`,
`trajectory`).

Authenticated requests send `Authorization: Bearer <access_token>`.

## YouTube channel data

`POST /auth/signup` now requires `channel_url` (a `youtube.com` URL — the
frontend's Sign Up form has a required field for it). Right after creating
the account, the backend fetches that channel from the **YouTube Data API
v3** (`app/services/youtube.py`) and stores title, description, thumbnail,
banner, country, published date, view/video/subscriber counts on the user.
It also feeds real subscriber/view numbers into the same `subscribers` /
`monthly_views` fields the forecast engine and Dashboard use.

**This needs `YOUTUBE_API_KEY` set in `.env`** — get one free at
https://console.cloud.google.com (create a project, enable "YouTube Data API
v3" under APIs & Services, create an API key under Credentials). Without a
key, signup still succeeds — the fetch just fails gracefully and
`channel_fetch_error` explains why; the user can retry from the Channel page
in the frontend (`POST /channel/refresh`) once a key is configured.

Channel URL formats handled: `/channel/UC...`, `/@handle`, `/user/name`, and
best-effort for legacy `/c/CustomName` (tries it as a handle, then falls back
to a search — the only reliable way to resolve those without a first-party
custom-URL lookup endpoint).

## Notifications

`app/services/notifications.py`'s `notify(db, user_id, type, title, message)`
is called from a few places to create real, persisted notifications: signup
(welcome + channel fetch outcome), `POST /channel/refresh` (fetch outcome),
and `POST /predictions` when a forecast completes (not for drafts). The
frontend's bell icon polls `GET /notifications` and shows an unread badge.

All timestamps sent to the frontend go through a `UTCDatetime` type
(`app/schemas.py`) that stamps an explicit UTC offset on serialization —
without it, naive `datetime.utcnow()` values serialize with no offset at all,
and `new Date(...)` in the browser silently misinterprets them as local time
(a real bug this project hit: "just now" notifications showed as "6 hours
ago"). Any new response field holding a `datetime` should use `UTCDatetime`
too, not the bare type.

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
    channel.py        /channel/* — also owns apply_channel_fetch(), called from signup
    dashboard.py      /dashboard/*
    predictions.py    /predictions/*
    trends.py         /trends/*
  services/
    prediction_engine.py   Mock forecast generator — TODO: real model here
    youtube.py              YouTube Data API v3 client + URL parsing
  utils/
    files.py          Upload handling (size limits, unique filenames)
```

## Connecting the frontend

The frontend (`../frontend`) is wired up to this API — see
`frontend/src/lib/api.js` and `frontend/src/context/AuthContext.jsx`. Run
both (backend first) and the Sign In/Sign Up/Dashboard/New
Prediction/Prediction Result screens all use real data end to end. CORS is
already configured for `http://localhost:5173` via `CORS_ORIGINS` in `.env`.
