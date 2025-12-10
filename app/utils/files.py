import os
from uuid import uuid4
from pathlib import Path
from PIL import Image, UnidentifiedImageError

MEDIA_ROOT = Path("media/pets")

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024

def ensure_media_dir():
    os.makedirs(MEDIA_ROOT, exist_ok=True)

def secure_filename(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    name = uuid4().hex
    return f"{name}{ext}"

def validate_image_and_save(upload_file, dest_path: Path):

    contents = upload_file.file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise ValueError("File too large")

    ext = Path(upload_file.filename).suffix.lower()
    if ext not in ALLOWED_EXT:
        raise ValueError("Unsupported file extension")
    from io import BytesIO
    try:
        img = Image.open(BytesIO(contents))
        img.verify()
    except UnidentifiedImageError:
        raise ValueError("Uploaded file is not a valid image")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(contents)
    return True
