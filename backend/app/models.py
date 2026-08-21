from datetime import datetime, date, time

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    # Channel stats used as the baseline for prediction forecasts. Seeded
    # from the real YouTube channel data below when the fetch succeeds;
    # otherwise these fall back to placeholder defaults and stay editable
    # from Settings.
    subscribers: Mapped[int] = mapped_column(Integer, default=1_200_000)
    monthly_views: Mapped[int] = mapped_column(Integer, default=45_800_000)

    # The channel URL is required at signup. Everything else here is
    # populated by app.services.youtube fetching the YouTube Data API v3 —
    # see app/routers/channel.py. A failed fetch (bad URL, no API key,
    # channel not found, quota) doesn't block signup; channel_fetch_error
    # records why, and the user can retry from the Channel page.
    channel_url: Mapped[str] = mapped_column(String(500))
    channel_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    channel_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    channel_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    channel_thumbnail_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    channel_banner_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    channel_country: Mapped[str | None] = mapped_column(String(10), nullable=True)
    channel_published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    channel_view_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    channel_video_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    channel_subscriber_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    channel_fetch_error: Mapped[str | None] = mapped_column(String(500), nullable=True)
    channel_fetched_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

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
