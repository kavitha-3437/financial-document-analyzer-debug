from pdfminer.high_level import extract_text
from pathlib import Path
import tempfile
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Robustly extract text from PDF bytes; returns "" on failure.
    """
    try:
        # write to temp file for pdfminer
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
            tmp.write(pdf_bytes)
            tmp.flush()
            text = extract_text(tmp.name) or ""
            # normalize whitespace
            text = " ".join(text.split())
            return text
    except Exception:
        logger.exception("PDF extraction failed")
        return ""
 
