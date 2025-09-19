import os
import requests
from dotenv import load_dotenv
load_dotenv()

CREWAI_API_KEY = os.getenv("CREWAI_API_KEY")
CREWAI_API_URL = os.getenv("CREWAI_API_URL")

class CrewAIClient:
    """
    Minimal wrapper for making deterministic calls to CrewAI (or similar).
    This expects the API to accept a JSON payload { "prompt": "...", "max_tokens": N, "temperature": T }.
    Adjust as required for the real CrewAI API.
    """
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or CREWAI_API_KEY
        self.base_url = base_url or CREWAI_API_URL
        if not self.api_key or not self.base_url:
            raise RuntimeError("CREWAI_API_KEY and CREWAI_API_URL must be set in environment")

    def run(self, prompt: str, max_tokens: int = 800, temperature: float = 0.0):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"prompt": prompt, "max_tokens": max_tokens, "temperature": temperature}
        resp = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.text
 
