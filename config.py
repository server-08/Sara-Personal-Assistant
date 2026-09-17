"""SARA — Config: .env loader + constants"""

import os
import sys

from dotenv import load_dotenv
from rich.console import Console

from errors import MissingAPIKeyError

# Load .env
load_dotenv()

# ---- Constants ----
MODEL = "gpt-4o-mini"
MAX_HISTORY = 10
TEMPERATURE = 0.7
MAX_INPUT_CHARS = 2000
MAX_RETRIES = 3
RETRY_BASE_DELAY = 2  # seconds → 2s, 4s, 8s

SYSTEM_PROMPT = (
    "You are SARA, a friendly personal AI assistant created by Manoj. "
    "Reply in the same language the user uses (Hindi, English, or Hinglish). "
    "Be helpful, concise, and warm."
)


def get_api_key() -> str:
    """API key load karo. Missing ho toh friendly error + exit."""
    key = os.getenv("API_KEY", "").strip()
    if not key:
        console = Console()
        console.print("[bold red]❌ API key nahi mili![/bold red]")
        console.print("[yellow]Fix:[/yellow] project folder me [.env] file banao:")
        console.print('    [cyan]API_KEY=sk-xxxx[/cyan]')
        sys.exit(1)
    return key
