import json
from celery_app import celery
from analysis import analyze_document
from models import save_analysis_result
import base64
import logging

logger = logging.getLogger(__name__)

@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 3})
def analyze_document_task(self, document_base64, metadata):
    """
    document_base64: base64-encoded PDF bytes
    metadata: dict with optional info like filename, uploader
    """
    try:
        # Call analysis (returns dict)
        result = analyze_document(document_base64, metadata)
        # Persist
        record_id = save_analysis_result(result, metadata)
        result['_db_id'] = record_id
        return result
    except Exception as e:
        logger.exception("Task failed")
        raise
 
