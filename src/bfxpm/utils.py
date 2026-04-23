import typer
from pathlib import Path
from rich.console import Console

console = Console()

def smart_prompt(text, default=None, password=False):
    """A wrapper for typer.prompt that handles 'exit', 'q', and 'abort' to terminate cleanly."""
    val = typer.prompt(text, default=default, hide_input=password)
    if str(val).lower() in ["q", "exit", "abort"]:
        console.print("\n[yellow]Aborted by user.[/yellow]")
        raise typer.Exit()
    return val

def smart_confirm(text, default=True):
    """A wrapper for interactive confirmation that handles 'exit', 'q', and 'abort'."""
    suffix = " [Y/n]" if default else " [y/N]"
    val = typer.prompt(f"{text}{suffix}", default="y" if default else "n")
    if str(val).lower() in ["q", "exit", "abort"]:
        console.print("\n[yellow]Aborted by user.[/yellow]")
        raise typer.Exit()
    return str(val).lower() in ("y", "yes", "true", "1")

def get_project_dir():
    """Find the project root by looking for .bfxpm directory."""
    curr = Path.cwd()
    # 1. Look up (current and parents)
    for parent in [curr] + list(curr.parents):
        if (parent / ".bfxpm").exists():
            return parent
            
    # 2. Look down (immediate subdirectories)
    try:
        subprojects = [p for p in curr.iterdir() if p.is_dir() and (p / ".bfxpm").exists()]
        if len(subprojects) == 1:
            return subprojects[0]
    except PermissionError:
        pass
        
    return curr
