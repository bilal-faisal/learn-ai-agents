import os
from rich import print
from typing import Final
from dotenv import load_dotenv

load_dotenv()

class MySecrets:
    """Loads and validates required environment variables"""

    gemini_api_key: Final[str]
    gemini_base_url: Final[str]
    gemini_model_name: Final[str]

    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY') or ""
        self.gemini_base_url = os.getenv('GEMINI_BASE_URL') or ""
        self.gemini_model_name = os.getenv('GEMINI_MODEL_NAME') or ""

        self._validate()

    def _validate(self):
        missing = []
        if not self.gemini_api_key:
            missing.append("GEMINI_API_KEY")
        if not self.gemini_base_url:
            missing.append("GEMINI_BASE_URL")
        if not self.gemini_model_name:
            missing.append("GEMINI_MODEL_NAME")

        if missing:
            for var in missing:
                print(f"[bold red]Error: {var} is not set in the environment variables.[/bold red]")
            raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")