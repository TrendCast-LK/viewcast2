from datetime import date, time

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Prediction, User
from app.schemas import PredictionOut, PredictionSummary
from app.services.prediction_engine import generate_forecast
from app.utils.files import save_upload, to_url

router = APIRouter(prefix="/predictions", tags=["predictions"])


def _to_out(prediction: Prediction) -> PredictionOut:
    return PredictionOut(
        id=prediction.id,
        title=prediction.title,
        category=prediction.category,
        tags=prediction.tags or [],
        target_date=prediction.target_date,
        target_time=prediction.target_time,
        thumbnail_url=to_url(prediction.thumbnail_path),
        status=prediction.status,
        predicted_views=prediction.predicted_views,
        confidence=prediction.confidence,
        change_vs_avg=prediction.change_vs_avg,
        trajectory=prediction.trajectory or [],
        created_at=prediction.created_at,
    )


def _to_summary(prediction: Prediction) -> PredictionSummary:
    return PredictionSummary(
        id=prediction.id,
        title=prediction.title,
        category=prediction.category,
        status=prediction.status,
        predicted_views=prediction.predicted_views,
        thumbnail_url=to_url(prediction.thumbnail_path),
        created_at=prediction.created_at,
    )


@router.post("", response_model=PredictionOut, status_code=status.HTTP_201_CREATED)
async def create_prediction(
    title: str = Form(...),
    category: str | None = Form(None),
    tags: str = Form(""),  # comma-separated, e.g. "Revenue,Q4"
    target_date: date | None = Form(None),
    target_time: time | None = Form(None),
    save_as_draft: bool = Form(False),
    thumbnail: UploadFile | None = File(None),
    dataset: UploadFile | None = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]

    try:
        thumbnail_path = await save_upload(thumbnail, subdir="thumbnails")
        dataset_path = await save_upload(dataset, subdir="datasets")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(exc)) from exc

    prediction = Prediction(
        owner_id=current_user.id,
        title=title,
        category=category,
        tags=tag_list,
        target_date=target_date,
        target_time=target_time,
        thumbnail_path=thumbnail_path,
        dataset_path=dataset_path,
        status="draft" if save_as_draft else "complete",
    )

    if not save_as_draft:
        forecast = generate_forecast(
            title=title,
            category=category,
            tags=tag_list,
            baseline_monthly_views=current_user.monthly_views,
        )
        prediction.predicted_views = forecast.predicted_views
        prediction.confidence = forecast.confidence
        prediction.change_vs_avg = forecast.change_vs_avg
        prediction.trajectory = forecast.trajectory

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return _to_out(prediction)


@router.get("", response_model=list[PredictionSummary])
def list_predictions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    predictions = (
        db.query(Prediction)
        .filter(Prediction.owner_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )
    return [_to_summary(p) for p in predictions]


@router.get("/{prediction_id}", response_model=PredictionOut)
def get_prediction(
    prediction_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    prediction = (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id, Prediction.owner_id == current_user.id)
        .first()
    )
    if prediction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found")
    return _to_out(prediction)


@router.delete("/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prediction(
    prediction_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    prediction = (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id, Prediction.owner_id == current_user.id)
        .first()
    )
    if prediction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found")
    db.delete(prediction)
    db.commit()
