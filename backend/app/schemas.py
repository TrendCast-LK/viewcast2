from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---- Auth / users -----------------------------------------------------


class UserCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


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
    created_at: datetime


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
    created_at: datetime


class PredictionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: str | None
    status: str
    predicted_views: int | None
    thumbnail_url: str | None
    created_at: datetime


# ---- Trends ---------------------------------------------------------------


class CategoryBreakdown(BaseModel):
    category: str
    count: int
    average_views: int


class TimelinePoint(BaseModel):
    id: int
    title: str
    created_at: datetime
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
