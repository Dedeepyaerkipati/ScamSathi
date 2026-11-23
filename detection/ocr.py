"""Optional local screenshot OCR via Tesseract.

Requires both the Python package pytesseract and the Tesseract OCR executable.
No image is sent to a third-party service.
"""
from __future__ import annotations
from io import BytesIO
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import pytesseract


def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract English text from a screenshot using locally installed Tesseract."""
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise ValueError("The uploaded file could not be read as an image.") from exc

    # Simple preprocessing can improve OCR on screenshots with low contrast.
    image = ImageOps.grayscale(image)
    image = ImageEnhance.Contrast(image).enhance(1.5)
    image = image.filter(ImageFilter.SHARPEN)
    try:
        return pytesseract.image_to_string(image, lang="eng", config="--psm 6").strip()
    except pytesseract.pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract OCR is not installed or is not on PATH. Install Tesseract for Windows, "
            "restart VS Code, and try again. See README.md."
        ) from exc
    except pytesseract.TesseractError as exc:
        raise RuntimeError(f"Tesseract could not process this image: {exc}") from exc
