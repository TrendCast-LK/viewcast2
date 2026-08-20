# ViewCast

A YouTube performance-prediction app, split into two projects:

| Folder | What |
| --- | --- |
| [`frontend/`](frontend) | React (Vite) app — the ViewCast UI (Sign In/Up, Dashboard, New Prediction, Prediction Results). See [frontend/README.md](frontend/README.md). |
| [`backend/`](backend) | FastAPI API — auth, predictions, mock forecast engine. See [backend/README.md](backend/README.md). |

The prediction ML model itself isn't integrated yet — the backend returns a
deterministic mock forecast in the meantime, and the frontend isn't wired up
to call the backend yet either (both are documented in their own READMEs).

## Quick start

```bash
# Frontend
cd frontend
npm install
npm run dev          # http://localhost:5173

# Backend (separate terminal)
cd backend
python -m venv .venv && .venv\Scripts\activate   # or `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000   # http://localhost:8000/docs
```
