from celery import Celery

from . import settings

app = Celery(
    main=settings.SYSTEM_CODENAME,
    # broker=settings.REDIS_BROKER_URL, # # TODO попробовать через RabbitMQ
)


class CeleryConfig:
    enable_utc = True
    timezone = 'Europe/Moscow'
    task_always_eager = settings.DEBUG
    task_serializer = "json"
    result_serializer = "json"
    beat_schedules = {}


app.config_from_object(CeleryConfig)
app.autodiscover_tasks(
    packages=[]
)
