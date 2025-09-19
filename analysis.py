import base64
import json
import os
from tools import extract_text_from_pdf_bytes
from agents import CrewAIClient
from prompt_templates import invoice_extraction_prompt
import logging
logger = logging.getLogger(__name__)

def decode_base64_document(doc_b64: str) -> bytes:
    try:
        return base64.b64decode(doc_b64)
    except Exception:
        logger.exception("Failed to decode base64 document")
        raise

def analyze_document(document_base64: str, metadata: dict) -> dict:
    """
    Orchestrates PDF -> text -> CrewAI prompt -> parse JSON.
    Returns a dict (parsed JSON or fallback).
    """
    pdf_bytes = decode_base64_document(document_base64)
    raw_text = extract_text_from_pdf_bytes(pdf_bytes)
    # Truncate to reasonable prompt length if needed
    max_chars = 30000
    doc_text = raw_text[:max_chars]
    prompt = invoice_extraction_prompt.format(document_text=doc_text)
    client = CrewAIClient()
    try:
        response_text = client.run(prompt=prompt, max_tokens=800, temperature=0.0)
    except Exception:
        logger.exception("CrewAI call failed")
        response_text = ""

    # Try to parse JSON robustly
    parsed = None
    if response_text:
        try:
            parsed = json.loads(response_text)
        except Exception:
            # Try to extract a JSON substring (best-effort)
            import re
            m = re.search(r"(\{.*\})", response_text, re.S)
            if m:
                try:
                    parsed = json.loads(m.group(1))
                except Exception:
                    logger.exception("Failed to parse JSON substring from model response")
    if parsed is None:
        parsed = {"error": "could_not_parse_model_output", "raw_output": response_text}

    parsed["raw_text"] = raw_text
    parsed["task_id"] = metadata.get("task_id") if metadata else None
    return parsed
 
