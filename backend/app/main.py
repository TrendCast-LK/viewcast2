from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
from app.routers import auth, dashboard, predictions, trends


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Scaffold-friendly: create tables on startup instead of running migrations.
    # Swap for Alembic migrations once the schema needs to evolve carefully.
    Base.metadata.create_all(bind=engine)
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(title="ViewCast API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# StaticFiles needs the directory to exist at mount time (before lifespan runs).
settings.upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(predictions.router)
app.include_router(trends.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
