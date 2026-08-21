from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import ChannelOut
from app.services.youtube import YouTubeError, fetch_channel_data

router = APIRouter(prefix="/channel", tags=["channel"])


def apply_channel_fetch(user: User, db: Session) -> None:
    """
    Fetch `user.channel_url` from YouTube and populate the channel_* fields.
    Never raises — a failure is recorded in channel_fetch_error so callers
    (signup, or the Channel page's Refresh button) can proceed regardless.
    """
    try:
        data = fetch_channel_data(user.channel_url)
    except YouTubeError as exc:
        user.channel_fetch_error = str(exc)
        user.channel_fetched_at = datetime.utcnow()
        db.add(user)
        db.commit()
        return

    user.channel_id = data.channel_id
    user.channel_title = data.title
    user.channel_description = data.description
    user.channel_thumbnail_url = data.thumbnail_url
    user.channel_banner_url = data.banner_url
    user.channel_country = data.country
    user.channel_published_at = data.published_at
    user.channel_view_count = data.view_count
    user.channel_video_count = data.video_count
    user.channel_subscriber_hidden = data.subscriber_hidden
    user.channel_fetch_error = None
    user.channel_fetched_at = datetime.utcnow()

    # Feed real numbers into the fields the forecast engine and Dashboard use.
    if data.subscriber_count is not None:
        user.subscribers = data.subscriber_count
    if data.view_count and data.published_at:
        months = max(1, (datetime.utcnow() - data.published_at).days / 30)
        user.monthly_views = round(data.view_count / months)

    db.add(user)
    db.commit()


def _to_out(user: User) -> ChannelOut:
    return ChannelOut(
        channel_url=user.channel_url,
        channel_id=user.channel_id,
        title=user.channel_title,
        description=user.channel_description,
        thumbnail_url=user.channel_thumbnail_url,
        banner_url=user.channel_banner_url,
        country=user.channel_country,
        published_at=user.channel_published_at,
        view_count=user.channel_view_count,
        subscriber_count=(
            user.subscribers if user.channel_id and not user.channel_subscriber_hidden else None
        ),
        subscriber_hidden=user.channel_subscriber_hidden,
        video_count=user.channel_video_count,
        fetch_error=user.channel_fetch_error,
        fetched_at=user.channel_fetched_at,
    )


@router.get("/me", response_model=ChannelOut)
def get_channel(current_user: User = Depends(get_current_user)):
    return _to_out(current_user)


@router.post("/refresh", response_model=ChannelOut)
def refresh_channel(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    apply_channel_fetch(current_user, db)
    db.refresh(current_user)
    return _to_out(current_user)
