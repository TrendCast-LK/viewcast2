from sqlalchemy.orm import Session

from app.models import Notification


def notify(db: Session, user_id: int, type: str, title: str, message: str) -> None:
    """Create a notification. Callers already own the commit for whatever
    else they're doing in the same request, so this commits on its own —
    a notification failing to save shouldn't roll back the real action."""
    db.add(Notification(owner_id=user_id, type=type, title=title, message=message))
    db.commit()
