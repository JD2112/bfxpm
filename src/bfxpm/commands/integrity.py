import typer
import hashlib
from pathlib import Path
from bfxpm.utils import console, get_project_dir

checksum_app = typer.Typer(help="Manage data integrity using checksums.")

def calculate_md5(file_path: Path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

@checksum_app.command("generate")
def generate():
    """Generate MD5 checksums for all files in the data directory."""
    d = get_project_dir()
    data_dir = d / "data"
    
    if not data_dir.exists():
        console.print("[red]No 'data/' directory found.[/red]")
        return
        
    checksum_file = d / "checksums.md5"
    console.print(f"[yellow]Generating checksums for {data_dir.relative_to(d)}...[/yellow]")
    
    with open(checksum_file, "w") as f:
        count = 0
        for p in data_dir.rglob("*"):
            if p.is_file():
                md5 = calculate_md5(p)
                f.write(f"{md5}  {p.relative_to(d)}\n")
                count += 1
                
    console.print(f"[bold green]✔ Generated {count} checksums in {checksum_file.name}[/bold green]")

@checksum_app.command("verify")
def verify():
    """Verify files against the checksums.md5 file."""
    d = get_project_dir()
    checksum_file = d / "checksums.md5"
    
    if not checksum_file.exists():
        console.print("[red]No checksums.md5 file found. Run 'bfxpm checksum generate' first.[/red]")
        return
        
    console.print("[yellow]Verifying data integrity...[/yellow]")
    
    success = 0
    fail = 0
    missing = 0
    
    with open(checksum_file, "r") as f:
        for line in f:
            if not line.strip(): continue
            expected_md5, rel_path = line.strip().split("  ")
            file_path = d / rel_path
            
            if not file_path.exists():
                console.print(f"[bold red]MISSING:[/bold red] {rel_path}")
                missing += 1
                continue
                
            actual_md5 = calculate_md5(file_path)
            if actual_md5 == expected_md5:
                success += 1
            else:
                console.print(f"[bold red]FAILED:[/bold red] {rel_path} (Mismatch!)")
                fail += 1
                
    if fail == 0 and missing == 0:
        console.print(f"[bold green]✔ Integrity check passed for {success} files.[/bold green]")
    else:
        console.print(f"\n[bold red]Integrity check failed![/bold red]")
        console.print(f"Passed: {success} | Failed: {fail} | Missing: {missing}")
