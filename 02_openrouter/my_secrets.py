import os
from rich import print
from typing import Final
from dotenv import load_dotenv

load_dotenv()

class MySecrets:
    """Loads and validates required environment variables"""

    openrouter_base_url: Final[str]
    openrouter_model: Final[str]
    openrouter_api_key: Final[str]

    def __init__(self):
        self.openrouter_base_url = os.getenv('OPENROUTER_BASE_URL') or ""
        self.openrouter_model = os.getenv('OPENROUTER_MODEL') or ""
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY') or ""

        self._validate()

    def _validate(self):
        missing = []
        if not self.openrouter_base_url:
            missing.append("OPENROUTER_BASE_URL")
        if not self.openrouter_model:
            missing.append("OPENROUTER_MODEL")
        if not self.openrouter_api_key:
            missing.append("OPENROUTER_API_KEY")

        if missing:
            for var in missing:
                print(f"[bold red]Error: {var} is not set in the environment variables.[/bold red]")
            raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")