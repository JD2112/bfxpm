import typer
import json
import shutil
from pathlib import Path
from datetime import datetime
from bfxpm.utils import console

def create_map(
    rollback: Path = typer.Option(None, "--rollback", "-r", "--reverse", help="JSON map file to revert the directory structure to"),
    force: bool = typer.Option(False, "--force", "-f", help="Move files without individual confirmation")
):
    """
    Create a map of the current directory structure OR rollback to a previous map.
    
    If no rollback file is provided, it creates a new snapshot.
    If a rollback file is provided, it attempts to move files back to their original locations recorded in that snapshot.
    """
    d = Path.cwd()
    
    # --- ROLLBACK LOGIC ---
    if rollback:
        if not rollback.exists():
            console.print(f"[bold red]Error:[/bold red] Map file {rollback} not found.")
            return
            
        console.print(f"[bold yellow]Initiating Rollback using {rollback.name}...[/bold yellow]")
        
        try:
            with open(rollback, "r") as f:
                data = json.load(f)
        except Exception as e:
            console.print(f"[bold red]Failed to read map file: {e}[/bold red]")
            return
            
        original_files = data.get("files", [])
        if not original_files:
            console.print("[red]No files found in the map.[/red]")
            return
            
        success_count = 0
        fail_count = 0
        
        # We need to find where these files are currently.
        # This is a bit "search intensive" but safe for bioinformatics projects.
        current_files_map = {}
        for p in d.rglob("*"):
            if p.is_file():
                current_files_map[p.name] = p
                
        for original_rel_path in original_files:
            orig_path = Path(original_rel_path)
            filename = orig_path.name
            
            # Find where it is now
            current_path = current_files_map.get(filename)
            
            if current_path:
                dest_path = d / orig_path
                
                # If it's already there, skip
                if current_path.resolve() == dest_path.resolve():
                    continue
                    
                if not force:
                    confirm = typer.confirm(f"Move {filename} back to {original_rel_path}?")
                    if not confirm:
                        continue
                
                # Ensure directory exists
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    shutil.move(str(current_path), str(dest_path))
                    success_count += 1
                except Exception as e:
                    console.print(f"[red]Error moving {filename}: {e}[/red]")
                    fail_count += 1
            else:
                console.print(f"[dim]Note: Could not find {filename} currently in the project.[/dim]")
                fail_count += 1
                
        console.print(f"\n[bold green]Rollback complete.[/bold green]")
        console.print(f"Moved: {success_count} files.")
        console.print(f"Failed/Missing: {fail_count} files.")
        return

    # --- MAPPING LOGIC ---
    console.print(f"[yellow]Mapping directory structure in {d}...[/yellow]")
    
    file_list = []
    count = 0
    for p in d.rglob("*"):
        if p.is_file():
            # Skip hidden files or specific directories to avoid noise
            if p.name.startswith(".") or ".git" in p.parts or ".bfxpm" in p.parts or "__pycache__" in p.parts:
                continue
            file_list.append(str(p.relative_to(d)))
            count += 1
            
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = d / f"bfxpm_structure_map_{timestamp}.json"
    
    with open(out_file, "w") as f:
        json.dump({
            "timestamp": timestamp,
            "directory": str(d),
            "files": file_list
        }, f, indent=2)
        
    console.print(f"[bold green]✔ Mapped {count} files to {out_file.name}[/bold green]")
    console.print("[dim]You can now safely run 'bfxpm organize' knowing your original structure is recorded.[/dim]")
