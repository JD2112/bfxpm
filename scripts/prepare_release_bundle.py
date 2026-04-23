#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

# Configuration: Define what stays and what goes
ESSENTIALS = [
    "src",            # Package source code
    "assets",         # Icons, templates, and logos
    "conda",          # Conda recipes
    "pyproject.toml",  # Build configuration
    "README.md",       # Documentation
    "LICENSE",         # Legal
]

STAGE_DIR = Path("release_stage")

def prepare_bundle():
    console.print(Panel.fit("🧹 BfxPM Clean Bundle Creator", style="bold cyan"))
    
    # 1. Fresh Start
    if STAGE_DIR.exists():
        console.print(f"[yellow]Removing existing {STAGE_DIR} directory...[/yellow]")
        shutil.rmtree(STAGE_DIR)
    STAGE_DIR.mkdir()

    console.print(f"📦 Creating pristine release bundle in [bold cyan]{STAGE_DIR}[/bold cyan]...")

    # 2. Copy Essentials
    for item in ESSENTIALS:
        src = Path(item)
        dest = STAGE_DIR / item
        
        if not src.exists():
            console.print(f"  [bold red]✖[/bold red] Warning: Essential item [bold]{item}[/bold] not found. Skipping.")
            continue

        if src.is_dir():
            shutil.copytree(src, dest)
            console.print(f"  [green]✔[/green] Copied directory: [bold]{item}[/bold]")
        else:
            shutil.copy2(src, dest)
            console.print(f"  [green]✔[/green] Copied file: [bold]{item}[/bold]")

    # 3. Final Verification
    console.print(f"\n[bold green]✨ Success![/bold green] Your clean bundle is ready in [bold]{STAGE_DIR}/[/bold]")
    console.print(f"[dim]This folder is now free of .git, .venv, and other local artifacts.[/dim]")
    console.print(f"[yellow]To build from here:[/yellow] cd {STAGE_DIR} && python3 -m build")

if __name__ == "__main__":
    prepare_bundle()
