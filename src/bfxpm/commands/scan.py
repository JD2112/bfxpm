import typer
from rich.table import Table
from pathlib import Path
from bfxpm.utils import console

def scan(path: str = typer.Argument(".", help="Directory to scan")):
    """Scan a directory for files, summarizing extensions and disk usage."""
    d = Path(path).resolve()
    if not d.exists():
        console.print(f"[bold red]Path {d} does not exist.[/bold red]")
        return
        
    stats = {}
    for item in d.rglob("*"):
        if item.is_file() and '.git' not in item.parts and '.venv' not in item.parts:
            ext = item.suffix or "no_extension"
            stats.setdefault(ext, {"count": 0, "size": 0})
            stats[ext]["count"] += 1
            stats[ext]["size"] += item.stat().st_size
            
    table = Table(title=f"File Extension Scanner: {d.name}")
    table.add_column("Extension", justify="left", style="cyan")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Size (MB)", justify="right", style="yellow")
    
    for ext, data in sorted(stats.items(), key=lambda x: x[1]["size"], reverse=True):
        size_mb = data["size"] / (1024 * 1024)
        table.add_row(ext, str(data["count"]), f"{size_mb:.2f}")
        
    console.print(table)
