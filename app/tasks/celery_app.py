from celery import Celery

celery_app = Celery(
    "tasks",
    broker="pyamqp://guest@localhost//",
    backend="rpc://",
    include=["app.tasks.tasks"])