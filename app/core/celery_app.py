from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "ai_tracking_system",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.autodiscover_tasks(["app.tasks"])
celery_app.conf.update(
    include=["app.tasks.ai_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
