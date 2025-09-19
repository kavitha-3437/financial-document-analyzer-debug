import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery = Celery("worker", broker=redis_url, backend=redis_url)
celery.conf.task_routes = {"tasks.analyze_document_task": {"queue": "analysis"}}
celery.conf.task_annotations = {"tasks.analyze_document_task": {"rate_limit": "10/s"}}
 
