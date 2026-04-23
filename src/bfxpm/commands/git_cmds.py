import typer
from rich.table import Table
from git import Repo
from bfxpm.utils import console, get_project_dir

def save(msg: str):
    """
    Save (version control) your scripts and config.
    
    This command acts as a wrapper around Git. It automatically tracks all new or modified 
    project files (like code, config, documentation) and creates a permanent commit/snapshot 
    with your provided message so you can easily revert to this milestone later.
    """
    d = get_project_dir()
    try:
        repo = Repo(d)
        repo.git.add(A=True)
        repo.index.commit(msg)
        console.print(f"[bold green]✔ Saved snapshot:[/bold green] {msg}")
    except Exception as e:
        console.print(f"[bold red]Version control failed. Is this a Git repo? {e}[/bold red]")

def history(limit: int = typer.Option(10, "--limit", "-l", help="Number of commits to show")):
    """
    View a beautiful timeline of script modifications with usage details.
    
    This provides an easy-to-read log of all your previous `bfxpm save` snapshots. 
    It displays the Git commit hash, the author, the exact date, and the descriptive 
    message you saved for that milestone, allowing you to track project progress.
    """
    d = get_project_dir()
    try:
        repo = Repo(d)
        commits = list(repo.iter_commits())
        
        table = Table(title="Project Modification History")
        table.add_column("Hash", style="dim cyan")
        table.add_column("Author", style="magenta")
        table.add_column("Date", justify="left", style="green")
        table.add_column("Message", style="yellow")
        
        for c in commits[:limit]:
            table.add_row(
                c.hexsha[:7], 
                str(c.author),
                c.committed_datetime.strftime("%Y-%m-%d %H:%M"), 
                c.summary
            )
        console.print(table)
    except Exception as e:
         console.print(f"[bold red]History unavailable: {e}[/bold red]")

def sync(
    data: bool = typer.Option(False, "--data", help="Also sync the 'data/' folder using rsync"),
    remote_path: str = typer.Option(None, "--remote", help="Remote SSH path for data sync (e.g. user@hpc:/path/to/project)")
):
    """
    Sync your project progress (Git) and optionally your large data folder (Rsync).
    
    By default, this wraps `git push` to backup your code and configs. 
    Use the `--data` option to also sync the large files in your `data/` directory 
    (which are usually ignored by Git) to a remote SSH endpoint or cluster using `rsync`.
    """
    d = get_project_dir()
    
    # 1. Git Sync
    try:
        repo = Repo(d)
        console.print("[yellow]Syncing Git repository...[/yellow]")
        origin = repo.remotes.origin
        origin.push()
        console.print("[bold green]✔ Git sync successful.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Git sync failed. Check remote network/origin setup: {e}[/bold red]")

    # 2. Data Sync (Rsync)
    if data:
        if not remote_path:
            console.print("[bold red]Error:[/bold red] --remote path is required for data sync.")
            raise typer.Exit(1)
            
        import subprocess
        data_path = d / "data"
        if not data_path.exists():
            console.print("[yellow]No 'data/' folder to sync.[/yellow]")
            return
            
        console.print(f"[yellow]Syncing data to {remote_path} via Rsync...[/yellow]")
        try:
            # -a: archive mode, -v: verbose, -z: compress, -P: partial/progress
            subprocess.run(["rsync", "-avzP", str(data_path) + "/", remote_path + "/data/"], check=True)
            console.print("[bold green]✔ Data sync successful.[/bold green]")
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Data sync failed: {e}[/bold red]")
