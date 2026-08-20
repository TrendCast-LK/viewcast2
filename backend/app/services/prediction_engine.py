"""
Forecast generation for a new prediction.

This is a MOCK implementation — it fabricates a plausible-looking 7-day view
trajectory so the rest of the stack (API, frontend) has real data shapes to
work with end to end. There is no machine learning happening here yet.

--------------------------------------------------------------------------
TODO(model integration): replace the body of `generate_forecast` with a call
into the real prediction model, e.g.:

    from app.services import model_client

    def generate_forecast(title, category, tags, thumbnail_path, dataset_path, baseline_monthly_views):
        return model_client.predict(
            title=title,
            category=category,
            tags=tags,
            thumbnail_path=thumbnail_path,
            dataset_path=dataset_path,
        )

The return shape (see `ForecastResult`) should stay the same so callers
(app/routers/predictions.py) don't need to change.
--------------------------------------------------------------------------
"""

from dataclasses import dataclass
import hashlib
import random


@dataclass
class ForecastResult:
    predicted_views: int
    confidence: float  # 0.0 - 1.0
    change_vs_avg: float  # percentage, e.g. 24.0 means +24%
    trajectory: list[dict]  # [{"day": "Day 1", "views": 150000}, ...]


def _seed_from(*parts: str | None) -> int:
    """Deterministic seed so the same inputs always produce the same mock forecast."""
    key = "|".join(p or "" for p in parts)
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def generate_forecast(
    title: str,
    category: str | None = None,
    tags: list[str] | None = None,
    baseline_monthly_views: int = 45_800_000,
    days: int = 7,
) -> ForecastResult:
    rng = random.Random(_seed_from(title, category, *(tags or [])))

    # Rough per-video ceiling derived from the channel's baseline, nudged by
    # the title length and a random factor — stands in for "the model".
    baseline_per_video = max(baseline_monthly_views / 30, 50_000)
    ceiling = baseline_per_video * rng.uniform(0.8, 3.5)

    trajectory: list[dict] = []
    views = 0.0
    for day in range(1, days + 1):
        # Diminishing-returns growth curve (fast early growth, tapering off),
        # plus a little day-to-day noise.
        progress = day / days
        eased = 1 - (1 - progress) ** 2
        target = ceiling * eased
        views += (target - views) * rng.uniform(0.55, 0.85)
        views = max(views, 0)
        trajectory.append({"day": f"Day {day}", "views": int(views)})

    predicted_views = trajectory[-1]["views"]
    change_vs_avg = round(((predicted_views - baseline_per_video) / baseline_per_video) * 100, 1)
    confidence = round(rng.uniform(0.68, 0.96), 2)

    return ForecastResult(
        predicted_views=predicted_views,
        confidence=confidence,
        change_vs_avg=change_vs_avg,
        trajectory=trajectory,
    )
