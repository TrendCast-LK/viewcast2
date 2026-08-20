from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Prediction, User
from app.schemas import CategoryBreakdown, TimelinePoint, TrendsSummary

router = APIRouter(prefix="/trends", tags=["trends"])


@router.get("/summary", response_model=TrendsSummary)
def summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    predictions = (
        db.query(Prediction)
        .filter(Prediction.owner_id == current_user.id)
        .order_by(Prediction.created_at.asc())
        .all()
    )

    completed = [p for p in predictions if p.status == "complete" and p.predicted_views is not None]
    draft_count = sum(1 for p in predictions if p.status == "draft")

    average_predicted_views = (
        round(sum(p.predicted_views for p in completed) / len(completed)) if completed else None
    )
    confidences = [p.confidence for p in completed if p.confidence is not None]
    average_confidence = round(sum(confidences) / len(confidences), 2) if confidences else None

    by_category: dict[str, list[int]] = defaultdict(list)
    for p in completed:
        by_category[p.category or "Uncategorized"].append(p.predicted_views)

    category_breakdown = [
        CategoryBreakdown(category=cat, count=len(views), average_views=round(sum(views) / len(views)))
        for cat, views in by_category.items()
    ]
    category_breakdown.sort(key=lambda c: c.average_views, reverse=True)

    best_category = category_breakdown[0].category if category_breakdown else None

    timeline = [
        TimelinePoint(id=p.id, title=p.title, created_at=p.created_at, predicted_views=p.predicted_views)
        for p in completed[-10:]
    ]

    return TrendsSummary(
        total_predictions=len(predictions),
        completed_predictions=len(completed),
        draft_predictions=draft_count,
        average_predicted_views=average_predicted_views,
        average_confidence=average_confidence,
        best_category=best_category,
        category_breakdown=category_breakdown,
        timeline=timeline,
    )
