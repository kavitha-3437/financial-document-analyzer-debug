invoice_extraction_prompt = """
SYSTEM:
You are a deterministic JSON extractor for invoices. ALWAYS return valid JSON and nothing else.

SCHEMA:
{{
  "invoice_number": string or null,
  "invoice_date": "YYYY-MM-DD" or null,
  "supplier": {{"name": string or null, "gstin": string or null}},
  "buyer": {{"name": string or null, "gstin": string or null}},
  "total_amount": float or null,
  "tax_amount": float or null,
  "currency": 3-letter code or null,
  "line_items": [{{"description": string or null, "quantity": int or null, "unit_price": float or null, "amount": float or null}}]
}}

RULES:
- If a field is missing, set its value to null.
- Use ISO dates (YYYY-MM-DD).
- Numbers must be plain numerics (no currency symbol).
- Output must be valid JSON only.

USER:
Document text:
\"\"\"{document_text}\"\"\"

Return JSON only following the SCHEMA exactly.
"""
 
