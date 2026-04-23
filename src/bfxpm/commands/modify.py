import typer
import shutil
from pathlib import Path
from bfxpm.utils import console, get_project_dir

def modify(
    source: str = typer.Argument(..., help="Path to the file or directory to move"),
    destination: str = typer.Argument(..., help="Destination path or project directory to move into")
):
    """Manually move any files or directories to a new location."""
    d = get_project_dir()
    
    source_path = Path(source)
    if not source_path.is_absolute():
        source_path = d / source_path
        
    dest_path = Path(destination)
    if not dest_path.is_absolute():
        dest_path = d / dest_path
        
    if not source_path.exists():
        console.print(f"[bold red]Error:[/bold red] Source '{source}' does not exist.")
        raise typer.Exit(1)
        
    # If destination is a directory that already exists, moving it inside
    if dest_path.is_dir():
        dest_path = dest_path / source_path.name
        
    # Ensure parent dir exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        shutil.move(str(source_path), str(dest_path))
        console.print(f"[bold green]✔[/bold green] Moved '{source_path.name}' to '{dest_path}'")
    except Exception as e:
        console.print(f"[bold red]Failed to move:[/bold red] {e}")
        raise typer.Exit(1)
