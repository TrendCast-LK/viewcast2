import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config import settings

# Keep uploads bounded — this is a scaffold, not a production media pipeline.
MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # 50MB, matches the frontend's copy ("Max 50MB")


async def save_upload(file: UploadFile | None, subdir: str) -> str | None:
    """Save an uploaded file under uploads/<subdir>/ and return its relative path, or None."""
    if file is None or not file.filename:
        return None

    dest_dir = settings.upload_dir / subdir
    dest_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(file.filename).suffix
    filename = f"{uuid.uuid4().hex}{suffix}"
    dest_path = dest_dir / filename

    size = 0
    with open(dest_path, "wb") as out_file:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_UPLOAD_BYTES:
                out_file.close()
                dest_path.unlink(missing_ok=True)
                raise ValueError("File exceeds the 50MB upload limit")
            out_file.write(chunk)

    return f"{subdir}/{filename}"


def to_url(relative_path: str | None) -> str | None:
    if not relative_path:
        return None
    return f"/uploads/{relative_path}"
