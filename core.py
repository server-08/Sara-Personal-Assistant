"""SARA — AI Engine: OpenAI calls with retry/backoff"""

import time

from openai import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
    APITimeoutError,
)
from rich.console import Console

import config
from memory import Memory

console = Console()


class AIEngine:
    def __init__(self):
        self.client = OpenAI(api_key=config.get_api_key())
        self.memory = Memory()

    def ask(self, user_input: str) -> str:
        """User input → memory → API call → reply text. Retry logic built-in."""
        self.memory.add("user", user_input)
        messages = self.memory.get_messages()

        attempt = 0
        while True:
            try:
                response = self.client.chat.completions.create(
                    model=config.MODEL,
                    messages=messages,
                    temperature=config.TEMPERATURE,
                )
                reply = response.choices[0].message.content or "(empty reply)"
                self.memory.add("assistant", reply)
                return reply

            except AuthenticationError:
                console.print("[bold red]❌ API key galat hai![/bold red] "
                              "[yellow].env me sahi key daalo[/yellow]")
                raise SystemExit(1)

            except RateLimitError:
                attempt += 1
                if attempt >= config.MAX_RETRIES:
                    console.print("[bold red]❌ Rate limit — retries khatam. "
                                  "Thodi der baad try karo.[/bold red]")
                    return "Maaf kijiye, abhi limit hit ho gayi. Kuch der baad try karein."
                delay = config.RETRY_BASE_DELAY * (2 ** (attempt - 1))  # 2s→4s→8s
                console.print(f"[yellow]⏳ Limit hit! {delay}s baad retry ({attempt}/3)...[/yellow]")
                time.sleep(delay)

            except APIConnectionError:
                console.print("[red]🌐 Internet check karo... ek retry:[/red]")
                if self._one_retry(messages):
                    return self._last_reply
                return "Connection nahi ho paaya. Internet check karke dobara try karein."

            except APITimeoutError:
                console.print("[red]🕐 Server slow hai... ek retry:[/red]")
                if self._one_retry(messages):
                    return self._last_reply
                return "Server slow hai. Thodi der baad try karein."

            except APIStatusError as e:
                console.print(f"[red]❌ Server error [code {e.status_code}][/red]")
                self.memory._history.pop()  # failed turn history se hatao
                return "Server me problem hai. Please dobara try karein."

    def _one_retry(self, messages) -> bool:
        """Single retry for connection/timeout errors."""
        try:
            time.sleep(2)
            response = self.client.chat.completions.create(
                model=config.MODEL, messages=messages, temperature=config.TEMPERATURE
            )
            self._last_reply = response.choices[0].message.content or "(empty reply)"
            self.memory.add("assistant", self._last_reply)
            return True
        except Exception:
            self.memory._history.pop()
            return False
