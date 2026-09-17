"""SARA — Personal AI Assistant | Controller: chat loop + slash commands
Created by Manoj • v1.0.0 (Chat Bot Only)
"""

from rich.console import Console

import config
from core import AIEngine
from ui import (prompt_user, show_banner, show_goodbye, show_reply,
                show_thinking)

console = Console()

HELP_TEXT = """
[bold yellow]SARA Commands[/bold yellow]
  [cyan]/help[/cyan]   — Ye help dikhao
  [cyan]/clear[/cyan]  — Chat memory reset karo
  [cyan]/about[/cyan]  — SARA ke baare me
  [cyan]/exit[/cyan]   — Quit (ya 'exit'/'bye' likho, Ctrl+C/Ctrl+D bhi chalega)
"""

ABOUT_TEXT = """**SARA** — Personal AI Assistant v1.0.0
💬 Pure chat bot • OpenAI `gpt-4o-mini` • Last-10 memory
Created with ❤️ by **Manoj**
"""


def handle_command(cmd: str, engine: AIEngine) -> bool:
    """Slash command handle karo. True = loop continue, False = exit."""
    if cmd == "/help":
        console.print(HELP_TEXT)
    elif cmd == "/clear":
        engine.memory.clear()
        console.print("[green]🧹 Memory cleared![/green]\n")
    elif cmd == "/about":
        console.print(ABOUT_TEXT)
    elif cmd == "/exit":
        return False
    return True


def main() -> None:
    show_banner()
    engine = AIEngine()

    while True:
        try:
            user_input = prompt_user().strip()

            if not user_input:
                continue
            if user_input.lower() in ("exit", "bye"):
                break
            if user_input.startswith("/"):
                if not handle_command(user_input.lower(), engine):
                    break
                continue

            # Long input truncate (2000 chars)
            if len(user_input) > config.MAX_INPUT_CHARS:
                user_input = user_input[: config.MAX_INPUT_CHARS]
                console.print("[dim](input truncated to 2000 chars)[/dim]")

            with show_thinking():
                reply = engine.ask(user_input)

            show_reply(reply)

        except KeyboardInterrupt:  # Ctrl+C
            console.print("\n[yellow](Ctrl+C)[/yellow]")
            break
        except EOFError:           # Ctrl+D
            console.print()
            break

    show_goodbye()


if __name__ == "__main__":
    main()
