"""SARA — UI Layer: Rich banner, spinner, markdown"""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

console = Console()

BANNER_ART = r"""
  ____    _____
 / ___|  |  ___|   __ _ _ __ ___   ___
 \___ \  | |_     / _` | '_ ` _ \ / _ \
  ___) | |  _|   | (_| | | | | | |  __/
 |____/  |_|      \__,_|_| |_| |_|\___|
"""

SARA_STYLE = "bold green"     # SARA prompt
USER_STYLE = "bold cyan"      # You prompt


def show_banner() -> None:
    art = Text(BANNER_ART, style="bold magenta")
    credit = Text("Created by Manoj", style="bold yellow", justify="right")
    console.print(Panel(art + "\n" + credit,
                        border_style="magenta", title="💬 SARA v1.0.0"))
    console.print("[dim]Type /help for commands • /exit ya Ctrl+C se bahar[/dim]\n")


def prompt_user() -> str:
    return console.input(f"[{USER_STYLE}]You ❯[/{USER_STYLE}] ")


def show_thinking():
    """Spinner context-manager return karo."""
    return console.status("[yellow]SARA soch rahi hai...[/yellow]", spinner="dots")


def show_reply(text: str) -> None:
    console.print(f"[bold green]SARA ❯[/bold green]")
    console.print(Markdown(text))
    console.print()


def show_goodbye() -> None:
    console.print("[magenta]👋 Goodbye! SARA says bye![/magenta]")
