from celery import Celery

from app.config import settings

if settings.MODE == "TEST":
    rabbit = settings.LOCAL_RABBIT
else:
    rabbit = settings.RABBIT


celery_app = Celery(
    "tasks",
    broker=f"pyamqp://guest@{rabbit}//",
    backend="rpc://",
    include=["app.tasks.tasks"])