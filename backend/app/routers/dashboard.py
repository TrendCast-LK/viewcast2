from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Prediction, User
from app.schemas import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    prediction_count = (
        db.query(Prediction).filter(Prediction.owner_id == current_user.id).count()
    )
    return DashboardSummary(
        full_name=current_user.full_name,
        subscribers=current_user.subscribers,
        monthly_views=current_user.monthly_views,
        prediction_count=prediction_count,
    )
