"""
Fetches public channel data from the YouTube Data API v3, given whatever
channel URL format a user pastes in at signup.

Requires YOUTUBE_API_KEY (see app/config.py). Get one at
https://console.cloud.google.com — create a project, enable "YouTube Data
API v3" under APIs & Services, then create an API key under Credentials.
"""

from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlparse

import httpx

from app.config import settings

API_BASE = "https://www.googleapis.com/youtube/v3"


class YouTubeError(Exception):
    """Raised for any channel-lookup failure; `str(exc)` is user-facing."""


@dataclass
class ChannelData:
    channel_id: str
    title: str
    description: str
    thumbnail_url: str | None
    banner_url: str | None
    country: str | None
    published_at: datetime | None
    view_count: int | None
    subscriber_count: int | None
    subscriber_hidden: bool
    video_count: int | None


def _parse_channel_url(url: str) -> dict:
    """Identify the lookup key from common YouTube channel URL shapes."""
    candidate = url.strip()
    if not candidate:
        raise YouTubeError("Channel URL is required.")
    if "://" not in candidate:
        candidate = f"https://{candidate}"

    parsed = urlparse(candidate)
    if "youtube.com" not in parsed.netloc and "youtu.be" not in parsed.netloc:
        raise YouTubeError("That doesn't look like a youtube.com channel URL.")

    parts = [p for p in parsed.path.split("/") if p]
    if not parts:
        raise YouTubeError("Couldn't find a channel name in that URL.")

    head = parts[0]
    if head == "channel" and len(parts) > 1:
        return {"id": parts[1]}
    if head.startswith("@"):
        return {"forHandle": head}
    if head == "user" and len(parts) > 1:
        return {"forUsername": parts[1]}
    if head == "c" and len(parts) > 1:
        # Legacy custom URLs (/c/Name) aren't directly resolvable by the API;
        # most also work as a handle, so try that first and fall back to search.
        return {"forHandle": f"@{parts[1]}", "searchFallback": parts[1]}

    # Bare name or unrecognized shape — best-effort handle guess, with search fallback.
    return {"forHandle": head if head.startswith("@") else f"@{head}", "searchFallback": head}


def _get(client: httpx.Client, path: str, params: dict) -> dict:
    response = client.get(f"{API_BASE}/{path}", params={**params, "key": settings.youtube_api_key})
    if response.status_code == 403:
        raise YouTubeError(
            "YouTube API refused the request (invalid key, API not enabled, or quota exceeded)."
        )
    if response.status_code != 200:
        raise YouTubeError(f"YouTube API error ({response.status_code}).")
    return response.json()


def _to_channel_data(item: dict) -> ChannelData:
    snippet = item.get("snippet", {})
    statistics = item.get("statistics", {})
    branding = item.get("brandingSettings", {}).get("image", {})

    thumbnails = snippet.get("thumbnails", {})
    thumbnail_url = (
        thumbnails.get("high", {}).get("url")
        or thumbnails.get("medium", {}).get("url")
        or thumbnails.get("default", {}).get("url")
    )

    published_at = None
    if snippet.get("publishedAt"):
        published_at = datetime.fromisoformat(snippet["publishedAt"].replace("Z", "+00:00")).replace(
            tzinfo=None
        )

    return ChannelData(
        channel_id=item["id"],
        title=snippet.get("title", ""),
        description=snippet.get("description", ""),
        thumbnail_url=thumbnail_url,
        banner_url=branding.get("bannerExternalUrl"),
        country=snippet.get("country"),
        published_at=published_at,
        view_count=int(statistics["viewCount"]) if "viewCount" in statistics else None,
        subscriber_count=(
            None if statistics.get("hiddenSubscriberCount") else int(statistics.get("subscriberCount", 0))
        ),
        subscriber_hidden=bool(statistics.get("hiddenSubscriberCount", False)),
        video_count=int(statistics["videoCount"]) if "videoCount" in statistics else None,
    )


def fetch_channel_data(channel_url: str) -> ChannelData:
    if not settings.youtube_api_key:
        raise YouTubeError(
            "No YOUTUBE_API_KEY configured on the server — see backend/.env.example."
        )

    lookup = _parse_channel_url(channel_url)
    search_fallback = lookup.pop("searchFallback", None)
    part = "snippet,statistics,brandingSettings"

    with httpx.Client(timeout=10) as client:
        data = _get(client, "channels", {"part": part, **lookup})
        items = data.get("items", [])

        if not items and search_fallback:
            search_data = _get(
                client,
                "search",
                {"part": "snippet", "type": "channel", "q": search_fallback, "maxResults": 1},
            )
            search_items = search_data.get("items", [])
            if search_items:
                found_id = search_items[0]["snippet"]["channelId"]
                data = _get(client, "channels", {"part": part, "id": found_id})
                items = data.get("items", [])

        if not items:
            raise YouTubeError("Couldn't find a YouTube channel at that URL.")

        return _to_channel_data(items[0])
