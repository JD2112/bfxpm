import typer
import shutil
import tarfile
from datetime import datetime
from pathlib import Path
from git import Repo
from bfxpm.utils import console, get_project_dir, smart_confirm

def compress(target: str = typer.Argument("intermediate", help="Folder to compress")):
    """Compress a large folder to tar.gz to save space."""
    d = get_project_dir()
    folder_map = {"intermediate": d / "intermediate", "data": d / "data", "scratch": d / "scratch"}
    
    target_path = folder_map.get(target, d / target)
    
    if not target_path.exists() or not target_path.is_dir():
        console.print(f"[bold red]Folder {target_path} not found.[/bold red]")
        raise typer.Exit(1)
        
    output_filename = f"{target_path.name}_compressed.tar.gz"
    output_path = target_path.parent / output_filename
    
    console.print(f"[yellow]Compressing {target_path} ...[/yellow]")
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(target_path, arcname=target_path.name)
        
    console.print(f"[bold green]✔ Compressed to {output_filename}.[/bold green]")
    if smart_confirm("Delete the original uncompressed folder?"):
        shutil.rmtree(target_path)
        console.print("[green]Original folder deleted.[/green]")

def login(token: str = typer.Argument(..., help="Your GitHub Personal Access Token or Cloud API key")):
    """Save GitHub/Cloud token locally."""
    cred_file = Path.home() / ".bfxpm_credentials"
    with open(cred_file, "w") as f:
         f.write(token)
    console.print("[bold green]✔ Logged in locally.[/bold green]")

def logout():
    """Remove locally saved credentials."""
    cred_file = Path.home() / ".bfxpm_credentials"
    if cred_file.exists():
        cred_file.unlink()
        console.print("[bold green]✔ Logged out.[/bold green]")
    else:
        console.print("[yellow]No credentials found.[/yellow]")

def run_history(save: bool = False):
    """Extract complex bioinformatics commands from shell history."""
    shells = [Path.home() / ".bash_history", Path.home() / ".zsh_history"]
    commands = []
    for shell in shells:
        if shell.exists():
            with open(shell, "r", errors='ignore') as f:
                lines = f.readlines()
                for line in lines[-100:]:
                    cmd = line.strip()
                    if cmd and not cmd.startswith(('cd ', 'ls', 'pwd', 'echo', 'clear', 'export', 'source')):
                        if cmd not in commands:
                            commands.append(cmd)
                            
    console.print("[bold cyan]Recent Complex Commands:[/bold cyan]")
    for c in commands[-15:]:
        console.print(f"[dim]{c}[/dim]")
        
    if save:
        d = get_project_dir()
        hist_file = d / "scripts" / "extracted_pipeline.sh"
        if hist_file.parent.exists():
            with open(hist_file, "w") as f:
                f.write("#!/bin/bash\n# Filtered history\n")
                for c in commands[-15:]:
                    f.write(c + "\n")
            console.print(f"[bold green]✔ Exported to {hist_file}[/bold green]")

def show():
    """Show all the hidden files in the project folder."""
    d = get_project_dir()
    console.print(f"[bold cyan]Hidden files in {d.name}:[/bold cyan]")
    count = 0
    for p in d.rglob(".*"):
        if p.is_file() and p.name.startswith("."):
            if ".git" in p.parts or ".bfxpm" in p.parts:
                continue
            console.print(f"  [dim]{p.relative_to(d)}[/dim]")
            count += 1
            
    if count == 0:
        console.print("[yellow]No hidden files found.[/yellow]")
    else:
        console.print(f"\n[bold green]Total:[/bold green] {count} hidden files")

import json
import yaml

def report():
    """Generate HTML/Markdown summary report and accompanying metadata files."""
    d = get_project_dir()
    report_md = d / "results" / "reports" / "PROJECT_SUMMARY.md"
    report_json = d / "results" / "reports" / "summary.json"
    report_yaml = d / "results" / "reports" / "summary.yml"
    
    if not report_md.parent.exists():
        report_md.parent.mkdir(parents=True)
        
    num_fastqs = len(list((d / "data").rglob("*.fastq*"))) if (d / "data").exists() else 0
    num_bams = len(list((d / "data").rglob("*.bam"))) + len(list((d / "results").rglob("*.bam"))) if (d / "data").exists() else 0
    total_size = sum(f.stat().st_size for f in d.rglob('*') if f.is_file()) / (1024*1024*1024) # in GB
    
    # Generate tree (simple version)
    # We will just write a representation or we could reuse internal tree logic.
    # For now simply listing directories:
    tree_out = []
    for p in sorted(d.glob("**/*")):
        if p.is_dir() and ".git" not in p.parts:
            tree_out.append(str(p.relative_to(d)))
            
    stats = {
        "generated_at": str(datetime.now()),
        "project_name": d.name,
        "metrics": {
            "num_fastqs": num_fastqs,
            "num_bams": num_bams,
            "total_size_gb": round(total_size, 2)
        },
        "directories": tree_out,
        "recent_history": []
    }
        
    report_content = f"# BfxPM Summary Report\nGenerated at: {datetime.now()}\n\n"
    report_content += "## Metrics\n"
    report_content += f"- **FASTQ Samples**: {num_fastqs}\n"
    report_content += f"- **BAM Alignments**: {num_bams}\n"
    report_content += f"- **Total Project Size**: {total_size:.2f} GB\n\n"
    
    try:
        repo = Repo(d)
        commits = list(repo.iter_commits())
        report_content += "## Recent History\n"
        for c in commits[:5]:
            report_content += f"- {c.committed_datetime.strftime('%Y-%m-%d')} : {c.summary}\n"
            stats["recent_history"].append({
                "date": c.committed_datetime.strftime('%Y-%m-%d'),
                "message": c.summary
            })
    except Exception:
        report_content += "No Git history available.\n"
        
    with open(report_md, "w") as f:
        f.write(report_content)
    
    # Prompt before overwriting README.md — back up to scratch first
    readme_path = d / "README.md"
    if readme_path.exists():
        if smart_confirm("Update the root README.md with the latest summary?"):
            scratch_dir = d / "scratch"
            scratch_dir.mkdir(parents=True, exist_ok=True)
            backup_name = f"README_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            shutil.copy(str(readme_path), str(scratch_dir / backup_name))
            console.print(f"[dim]Backed up existing README.md to scratch/{backup_name}[/dim]")
            with open(readme_path, "w") as f:
                f.write(report_content)
    else:
        with open(readme_path, "w") as f:
            f.write(report_content)

    with open(report_json, "w") as f:
        json.dump(stats, f, indent=4)
    with open(report_yaml, "w") as f:
        yaml.dump(stats, f)
        
    console.print(f"[bold green]✔ Reports generated in {report_md.parent.relative_to(d)} and root README.md updated.[/bold green]")
    
def list_projects(
    path: str = typer.Argument(".", help="Root directory to scan for projects"),
    html: bool = typer.Option(False, "--html", help="Generate an HTML summary of all projects")
):
    """Scan and list all BfxPM projects in the given directory."""
    from rich.table import Table
    root = Path(path).resolve()
    projects = []
    
    console.print(f"[yellow]Scanning {root} for BfxPM projects...[/yellow]")
    
    # We look for direct subdirectories that have project.yml or .bfxpm
    for item in root.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            config_file = item / "project.yml"
            is_bfxpm = (item / ".bfxpm").exists()
            
            if config_file.exists() or is_bfxpm:
                meta = {}
                if config_file.exists():
                    try:
                        with open(config_file, "r") as f:
                            meta = yaml.safe_load(f) or {}
                    except Exception:
                        pass
                
                stats = item.stat()
                created = datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d")
                modified = datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d")
                
                # Basic file counts to show activity (limit depth to avoid TB-scale lockups)
                try:
                    num_files = len(list(item.glob("*"))) + len(list(item.glob("*/*")))
                except Exception:
                    num_files = "N/A"
                
                projects.append({
                    "name": meta.get("project_name", item.name),
                    "path": str(item),
                    "created": created,
                    "modified": modified,
                    "author": meta.get("author", "Unknown"),
                    "files": num_files
                })
                    
    if not projects:
        console.print("[bold red]No BfxPM projects found.[/bold red]")
        return
        
    table = Table(title=f"BfxPM Projects Index")
    table.add_column("Project Name", style="bold cyan")
    table.add_column("Author", style="magenta")
    table.add_column("Created", style="green")
    table.add_column("Modified", style="yellow")
    table.add_column("Files", justify="right")
    table.add_column("Path", style="dim", overflow="fold")
    
    for p in projects:
        table.add_row(
            p["name"], 
            p["author"], 
            p["created"], 
            p["modified"], 
            str(p["files"]),
            p["path"]
        )
        
    console.print(table)

    if html:
        html_out = root / "projects_index.html"
        rows = ""
        for p in projects:
            rows += f"""
            <tr>
                <td><strong>{p['name']}</strong></td>
                <td>{p['author']}</td>
                <td>{p['created']}</td>
                <td>{p['modified']}</td>
                <td>{p['files']}</td>
                <td style="font-size: 0.8em; color: gray;">{p['path']}</td>
            </tr>
            """
        
        full_html = f"""
        <html>
        <head>
            <title>BfxPM Projects Index</title>
            <style>
                body {{ font-family: sans-serif; margin: 40px; background: #f9f9f9; }}
                table {{ width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
                th {{ background: #2c3e50; color: white; }}
                tr:hover {{ background: #f1f1f1; }}
                h1 {{ color: #2c3e50; }}
            </style>
        </head>
        <body>
            <h1>BfxPM Projects Index</h1>
            <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
            <table>
                <thead>
                    <tr>
                        <th>Project Name</th>
                        <th>Author</th>
                        <th>Created</th>
                        <th>Modified</th>
                        <th>File Count</th>
                        <th>Path</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </body>
        </html>
        """
        with open(html_out, "w") as f:
            f.write(full_html)
        console.print(f"\n[bold green]✔ HTML index generated at:[/bold green] {html_out}")

def update():
    """Update BfxPM to the latest version via pip."""
    import subprocess
    import sys
    from bfxpm import __version__
    
    console.print(f"[yellow]Current version: [bold]{__version__}[/bold][/yellow]")
    console.print("[yellow]Checking for updates...[/yellow]")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", "bfxpm"],
            capture_output=True, text=True
        )
        if "Successfully installed" in result.stdout:
            # Extract the new version from pip output
            for part in result.stdout.split():
                if part.startswith("bfxpm-"):
                    new_version = part.replace("bfxpm-", "")
                    console.print(f"[bold green]✔ Updated to version {new_version}[/bold green]")
                    break
            else:
                console.print("[bold green]✔ Update complete.[/bold green]")
        elif "already satisfied" in result.stdout.lower() or "already up-to-date" in result.stdout.lower():
            console.print(f"[bold green]✔ Already at the latest version ({__version__}).[/bold green]")
        else:
            console.print(f"[bold green]✔ Update complete.[/bold green]")
            
        if result.stderr:
            console.print(f"[dim]{result.stderr.strip()}[/dim]")
    except FileNotFoundError:
        console.print("[bold red]Error: pip not found. Please ensure pip is installed.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Update failed: {e}[/bold red]")
