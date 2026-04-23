import typer
import shutil
import subprocess
from bfxpm.utils import console, get_project_dir

fetch_app = typer.Typer(help="Fetch and route external biological data")

@fetch_app.command("sra")
def fetch_sra(srr: str):
    """Download SRA data using fastq-dump into data/raw_external/."""
    if not shutil.which("fastq-dump"):
        console.print("[bold red]Error: 'fastq-dump' is not installed or not in PATH.[/bold red]")
        console.print("[yellow]Please install the SRA-Toolkit to use this command.[/yellow]")
        return
        
    d = get_project_dir()
    outdir = d / "data" / "raw_external"
    outdir.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[cyan]Fetching SRA dataset {srr}...[/cyan]")
    try:
        subprocess.run(["fastq-dump", "--outdir", str(outdir), "--split-files", srr], check=True)
        console.print(f"[bold green]✔ Successfully downloaded {srr} to {outdir.relative_to(d)}[/bold green]")
    except subprocess.CalledProcessError:
        console.print(f"[bold red]Failed to download {srr}[/bold red]")

@fetch_app.command("ensembl")
def fetch_ensembl(build: str = typer.Argument(..., help="e.g. GRCh38")):
    """Download Ensembl references into data/references/."""
    if not shutil.which("wget") and not shutil.which("curl"):
        console.print("[bold red]Error: Neither 'wget' nor 'curl' is installed.[/bold red]")
        console.print("[yellow]Please install standard networking tools to fetch files.[/yellow]")
        return
        
    d = get_project_dir()
    outdir = d / "data" / "references"
    outdir.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[cyan]Fetching reference info for {build}... (Simulation)[/cyan]")
    # Here we would construct the Ensembl FTP URL and download.
    console.print("[yellow]This is a placeholder simulation for ensembl download.[/yellow]")
    console.print(f"[bold green]✔ Done creating placeholder in {outdir.relative_to(d)}[/bold green]")
