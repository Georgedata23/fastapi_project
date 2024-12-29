from PIL import Image
from pathlib import Path

from pydantic import PositiveInt
from pytesseract import pytesseract

from app.logging_dir.logging_file import logger
from app.tasks.celery_app import celery_app


@celery_app.task()
def img_to_text(id_doc: PositiveInt):
    image = Image.open(Path(f"app/doc_static/images/{id_doc}.webp"))
    extracted_text = pytesseract.image_to_string(image)
    logger.info("Текст считан!")
    return extracted_text
