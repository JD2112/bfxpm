import typer
import shutil
import zipfile
import webbrowser
import os
from pathlib import Path
from bfxpm.utils import console, get_project_dir, smart_confirm, smart_prompt

deposit_app = typer.Typer(help="Deposit data/code to public repositories (Zenodo, FigShare, etc.)")

REPOSITORIES = {
    "zenodo": "https://zenodo.org/deposit",
    "figshare": "https://figshare.com/account/home",
    "dataverse": "https://dataverse.org/",
    "dryad": "https://datadryad.org/stash",
    "mendeley": "https://data.mendeley.com/",
    "datahub": "https://datahub.io/",
    "dans": "https://dans.knaw.nl/en/",
    "eudat": "https://eudat.eu/services/b2share"
}

@deposit_app.callback()
def callback():
    """Commands for preparing and depositing project data to public repositories."""
    pass

@deposit_app.command(name="list")
def list_repositories():
    """List supported data repositories."""
    console.print("[bold cyan]Supported Repositories:[/bold cyan]")
    for repo in REPOSITORIES:
        console.print(f" - [bold]{repo.capitalize()}[/bold]: {REPOSITORIES[repo]}")

@deposit_app.command()
def prepare(
    output: Path = typer.Option("deposit_bundle.zip", "--output", "-o", help="Name of the zip bundle"),
    include_data: bool = typer.Option(True, "--include-data", help="Include the data/ folder?"),
    include_results: bool = typer.Option(True, "--include-results", help="Include the results/ folder?")
):
    """
    Produce a clean ZIP bundle of the project for deposition.
    
    This command creates a compressed archive of your project, excluding 
    unnecessary files like .git, .bfxpm, and temporary files. 
    It ensures your deposit is clean and ready for peer review.
    """
    d = get_project_dir()
    exclude_dirs = {".git", ".bfxpm", ".venv", "__pycache__", ".pytest_cache", ".DS_Store"}
    
    if not include_data:
        exclude_dirs.add("data")
    if not include_results:
        exclude_dirs.add("results")

    console.print(f"[yellow]Preparing deposit bundle: [bold]{output}[/bold]...[/yellow]")
    
    try:
        with zipfile.ZipFile(d / output, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(d):
                # Modify dirs in-place to skip excluded directories
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                
                for file in files:
                    if file in exclude_dirs or file == str(output):
                        continue
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(d)
                    zipf.write(file_path, rel_path)
                    
        console.print(f"[bold green]✔ Bundle created successfully:[/bold green] {d / output}")
        console.print(f"[dim]Size: {round((d / output).stat().st_size / (1024*1024), 2)} MB[/dim]")
    except Exception as e:
        console.print(f"[bold red]Failed to create bundle: {e}[/bold red]")

@deposit_app.command()
def go(repo: str = typer.Argument(..., help="Repository name (e.g., zenodo, figshare)")):
    """Open the deposit page for the chosen repository in your browser."""
    from rich.panel import Panel
    repo_lower = repo.lower()
    
    eu_based = ["zenodo", "dans", "eudat"]
    
    if repo_lower in REPOSITORIES:
        url = REPOSITORIES[repo_lower]
        location_msg = "EU-based but globally accessible" if repo_lower in eu_based else "Likely processors outside the EU"
        
        console.print(Panel(
            f"[bold yellow]Public Deposition Warning[/bold yellow]\n"
            f"You are about to open the [bold cyan]{repo.capitalize()}[/bold cyan] submission page.\n"
            f"Region/Status: [bold green]{location_msg}[/bold green]\n\n"
            "By choosing to deposit your data publicly, you must ensure you have the rights to share "
            "this data and that any sensitive/GDPR-protected person-identifiable info has been removed.",
            title="📂 Data Deposit Alert",
            border_style="yellow"
        ))
        
        confirm = smart_confirm(f"Do you want to proceed to the {repo.capitalize()} website?", default=False)
        if not confirm:
            console.print("[yellow]Deposition process cancelled by user.[/yellow]")
            return
            
        console.print(f"[yellow]Opening {repo.capitalize()} deposit page...[/yellow]")
        webbrowser.open(url)
    else:
        console.print(f"[bold red]Repository '{repo}' not found.[/bold red]")
        console.print("Run [bold cyan]bfxpm deposit list[/bold cyan] to see available options.")
