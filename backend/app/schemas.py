from datetime import date, datetime, time, timezone
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, PlainSerializer, field_validator


def _as_utc_iso(value: datetime) -> str:
    # Every datetime we store represents UTC (via datetime.utcnow()) but is
    # naive, so plain serialization omits the offset and browsers parsing it
    # with `new Date(...)` interpret it as *local* time instead — silently
    # shifting every timestamp in the UI by the viewer's UTC offset. Stamp
    # the UTC offset on the way out instead of fixing this at every callsite.
    aware = value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
    return aware.isoformat()


UTCDatetime = Annotated[datetime, PlainSerializer(_as_utc_iso, return_type=str)]


# ---- Auth / users -----------------------------------------------------


class UserCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    channel_url: str = Field(min_length=1, max_length=500)

    @field_validator("channel_url")
    @classmethod
    def validate_channel_url(cls, value: str) -> str:
        value = value.strip()
        if "youtube.com" not in value and "youtu.be" not in value:
            raise ValueError("Enter a youtube.com channel URL (e.g. https://www.youtube.com/@yourchannel)")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    subscribers: int
    monthly_views: int
    channel_url: str
    channel_title: str | None
    channel_thumbnail_url: str | None
    created_at: UTCDatetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class DashboardSummary(BaseModel):
    full_name: str
    subscribers: int
    monthly_views: int
    prediction_count: int


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    subscribers: int | None = Field(default=None, ge=0)
    monthly_views: int | None = Field(default=None, ge=0)


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class ChannelOut(BaseModel):
    channel_url: str
    channel_id: str | None
    title: str | None
    description: str | None
    thumbnail_url: str | None
    banner_url: str | None
    country: str | None
    published_at: UTCDatetime | None
    view_count: int | None
    subscriber_count: int | None
    subscriber_hidden: bool
    video_count: int | None
    fetch_error: str | None
    fetched_at: UTCDatetime | None


# ---- Notifications ----------------------------------------------------------


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    title: str
    message: str
    read: bool
    created_at: UTCDatetime


class NotificationList(BaseModel):
    unread_count: int
    notifications: list[NotificationOut]


# ---- Predictions --------------------------------------------------------


class TrajectoryPoint(BaseModel):
    day: str
    views: int


class PredictionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: str | None
    tags: list[str]
    target_date: date | None
    target_time: time | None
    thumbnail_url: str | None
    status: str
    predicted_views: int | None
    confidence: float | None
    change_vs_avg: float | None
    trajectory: list[TrajectoryPoint]
    created_at: UTCDatetime


class PredictionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: str | None
    status: str
    predicted_views: int | None
    thumbnail_url: str | None
    created_at: UTCDatetime


# ---- Trends ---------------------------------------------------------------


class CategoryBreakdown(BaseModel):
    category: str
    count: int
    average_views: int


class TimelinePoint(BaseModel):
    id: int
    title: str
    created_at: UTCDatetime
    predicted_views: int


class TrendsSummary(BaseModel):
    total_predictions: int
    completed_predictions: int
    draft_predictions: int
    average_predicted_views: int | None
    average_confidence: float | None
    best_category: str | None
    category_breakdown: list[CategoryBreakdown]
    timeline: list[TimelinePoint]
