from celery import Celery

celery_app = Celery(
    "tasks",
    broker="pyamqp://guest@rabbitmq//",
    backend="rpc://",
    include=["app.tasks.tasks"])