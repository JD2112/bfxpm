#!/usr/bin/env python3
import os
import shutil
import re
import subprocess
import datetime
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

console = Console()
app = typer.Typer(help="BfxPM Publishing & Release Automation")

def run_cmd(cmd: str, check: bool = True, cwd: Optional[str] = None):
    """Utility to run shell commands."""
    cwd_str = f" [dim](cwd: {cwd})[/dim]" if cwd else ""
    console.print(f"[bold blue]Executing:[/bold blue] {cmd}{cwd_str}")
    result = subprocess.run(cmd, shell=True, check=check, cwd=cwd)
    return result

def backup_and_clean(version: str):
    """Moves previous build artifacts to a backup folder."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = Path(".bfxpm/backups")
    backup_dir = backup_root / f"publish_v{version}_{timestamp}"
    
    dirty_dirs = ["dist", "build", "src/bfxpm.egg-info"]
    
    if any(os.path.exists(d) for d in dirty_dirs):
        if Confirm.ask("[yellow]Found previous build artifacts. Move to backup?[/yellow]"):
            backup_dir.mkdir(parents=True, exist_ok=True)
            for d in dirty_dirs:
                if os.path.exists(d):
                    shutil.move(d, backup_dir / os.path.basename(d))
            console.print(f"[green]✔ Backup created at:[/green] {backup_dir}")
    else:
        console.print("[dim]No previous build artifacts found.[/dim]")

def get_current_version() -> str:
    path = Path("pyproject.toml")
    content = path.read_text()
    match = re.search(r'version = "(.*?)"', content)
    return match.group(1) if match else "0.0.0"

def update_version_file(new_version: str):
    # Update pyproject.toml
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    new_content = re.sub(r'version = "(.*?)"', f'version = "{new_version}"', content)
    pyproject_path.write_text(new_content)
    console.print(f"[green]✔ Version updated to {new_version} in pyproject.toml[/green]")

    # Update conda/meta.yaml
    meta_path = Path("conda/meta.yaml")
    if meta_path.exists():
        meta_content = meta_path.read_text()
        new_meta = re.sub(r'{% set version = "(.*?)" %}', f'{{% set version = "{new_version}" %}}', meta_content)
        meta_path.write_text(new_meta)
        console.print(f"[green]✔ Version updated to {new_version} in conda/meta.yaml[/green]")

def check_dependencies(check_conda: bool = False):
    """Checks if build and twine are installed. Optionally checks conda tools."""
    deps = ["build", "twine"]
    missing = []
    
    # Check for build tool
    import subprocess
    for dep in deps:
        result = subprocess.run(f"python3 -c 'import {dep}'", shell=True, capture_output=True)
        if result.returncode != 0:
            missing.append(dep)
    
    if check_conda:
        # Check for conda-build and anaconda-client via shell
        for tool in ["conda-build", "anaconda"]:
            result = subprocess.run(f"which {tool}", shell=True, capture_output=True)
            if result.returncode != 0:
                missing.append(tool)
    
    if missing:
        console.print(f"[bold red]Error: Missing required publishing tools: {', '.join(missing)}[/bold red]")
        if "conda-build" in missing or "anaconda" in missing:
            console.print("[yellow]For Conda: Run 'conda install conda-build anaconda-client'[/yellow]")
        
        if Confirm.ask(f"Would you like to try installing the pip-based dependencies? (pip install ...)"):
            pip_deps = [d for d in missing if d not in ["conda-build", "anaconda"]]
            if pip_deps:
                run_cmd(f"python3 -m pip install {' '.join(pip_deps)}")
                console.print("[green]✔ Pip dependencies installed.[/green]")
                # Re-check to see if everything is now satisfied
                check_dependencies(check_conda=check_conda)
            else:
                console.print("[yellow]No pip-based dependencies found to install.[/yellow]")
                console.print("[bold red]Error:[/bold red] Required tools [bold]conda-build[/bold] or [bold]anaconda-client[/bold] are still missing.")
                console.print("Please run: [cyan]conda install conda-build anaconda-client[/cyan] manually.")
                raise typer.Exit(1)
        else:
            console.print("[yellow]Please install missing tools manually and try again.[/yellow]")
            raise typer.Exit(1)

@app.command()
def release():
    """Complete release workflow: Version -> Clean -> Build -> Publish -> Tag."""
    check_dependencies()
    console.print(Panel.fit("🚀 BfxPM Release Management System", style="bold magenta"))

    # 1. Versioning
    current_v = get_current_version()
    console.print(f"Current version: [bold cyan]{current_v}[/bold cyan]")
    
    bump = Prompt.ask(
        "Select version bump", 
        choices=["patch", "minor", "major", "manual", "skip"], 
        default="patch"
    )
    
    if bump == "skip":
        new_v = current_v
    elif bump == "manual":
        new_v = Prompt.ask("Enter new version string")
    else:
        parts = list(map(int, current_v.split('.')))
        if bump == "patch": parts[2] += 1
        elif bump == "minor": parts[1] += 1; parts[2] = 0
        elif bump == "major": parts[0] += 1; parts[1] = 0; parts[2] = 0
        new_v = ".".join(map(str, parts))

    if new_v != current_v:
        if Confirm.ask(f"Bump version to {new_v}?"):
            update_version_file(new_v)
        else:
            new_v = current_v

    # 2. Cleanup & Bundle Preparation
    use_stage = False
    if Confirm.ask("Create and use a pristine [bold cyan]release_stage[/bold cyan] for building?"):
        run_cmd("python3 scripts/prepare_release_bundle.py")
        use_stage = True
        build_cwd = "release_stage"
    else:
        backup_and_clean(new_v)
        build_cwd = None

    # 3. Build & PyPI
    if Confirm.ask("Build and Publish to [bold blue]PyPI[/bold blue]?"):
        run_cmd("python3 -m build", cwd=build_cwd)
        # Twine check needs the dist folder relative to where build was run
        dist_path = "dist/*"
        run_cmd(f"twine check {dist_path}", cwd=build_cwd)
        if Confirm.ask("Twine check passed. Proceed to upload?"):
            run_cmd(f"twine upload {dist_path}", cwd=build_cwd)

    # 4. Anaconda
    if Confirm.ask("Build and Publish to [bold green]Anaconda[/bold green]?"):
        check_dependencies(check_conda=True)
        run_cmd("conda build conda/ -c conda-forge", cwd=build_cwd)
        if Confirm.ask("Conda build complete. Proceed to anaconda upload?"):
            run_cmd("anaconda upload $(conda build conda/ -c conda-forge --output)", cwd=build_cwd)

    # 5. Git Tag & Push (Always from main root)
    if Confirm.ask("Commit changes, Tag and Push to [bold]GitHub[/bold]?"):
        run_cmd(f"git add pyproject.toml conda/meta.yaml")
        run_cmd(f'git commit -m "chore: release v{new_v}"')
        run_cmd(f"git tag -a v{new_v} -m 'Version {new_v} release'")
        run_cmd("git push origin main")
        run_cmd(f"git push origin v{new_v}")
        console.print(f"[bold green]✔ Release v{new_v} successfully pushed to GitHub![/bold green]")

    console.print(Panel.fit("✨ Release Workflow Complete ✨", style="bold green"))

if __name__ == "__main__":
    app()
