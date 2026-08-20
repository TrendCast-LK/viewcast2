# ViewCast

A YouTube performance-prediction app, split into two projects:

| Folder | What |
| --- | --- |
| [`frontend/`](frontend) | React (Vite) app — the ViewCast UI (Sign In/Up, Dashboard, New Prediction, Prediction Results). See [frontend/README.md](frontend/README.md). |
| [`backend/`](backend) | FastAPI API — auth, predictions, mock forecast engine. See [backend/README.md](backend/README.md). |

The frontend and backend are connected — real sign up/sign in, a real
Dashboard, and real predictions with a forecast (chart included) all flow
through the API below. The only thing still mocked is the ML model itself:
`backend/app/services/prediction_engine.py` generates a deterministic-looking
forecast instead of running a real model — that's the one piece left to wire
in later.

## Quick start

Run both — the frontend needs the backend to be up.

```bash
# Backend (terminal 1)
cd backend
python -m venv .venv && .venv\Scripts\activate   # or `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000   # http://localhost:8000/docs

# Frontend (terminal 2)
cd frontend
npm install
cp .env.example .env
npm run dev          # http://localhost:5173
```
