from datetime import datetime, date, time

from sqlalchemy import JSON, Date, DateTime, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    # Placeholder channel stats shown on the Dashboard screen until a real
    # YouTube-data integration exists.
    subscribers: Mapped[int] = mapped_column(Integer, default=1_200_000)
    monthly_views: Mapped[int] = mapped_column(Integer, default=45_800_000)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    predictions: Mapped[list["Prediction"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    title: Mapped[str] = mapped_column(String(255))
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)

    target_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    target_time: Mapped[time | None] = mapped_column(Time, nullable=True)

    thumbnail_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    dataset_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    status: Mapped[str] = mapped_column(String(20), default="complete")  # draft | complete

    # Forecast output. Populated by app.services.prediction_engine — currently
    # a mock, will be replaced by the real model's output later.
    predicted_views: Mapped[int | None] = mapped_column(Integer, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    change_vs_avg: Mapped[float | None] = mapped_column(Float, nullable=True)
    trajectory: Mapped[list[dict]] = mapped_column(JSON, default=list)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner: Mapped["User"] = relationship(back_populates="predictions")
