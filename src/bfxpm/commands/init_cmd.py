import typer
from pathlib import Path
from bfxpm.utils import console, smart_prompt, smart_confirm

def init_app():
    """Initialize a new BfxPM project including folder structures and Git repository."""
    import yaml
    import shutil
    import inspect
    from datetime import datetime
    from git import Repo

    header = inspect.cleandoc("""
         ┳┓•  ┏┓┳┳┓   ┳┓•  •  ┏          •    ┏┓    •      ┳┳┓            
         ┣┫┓┏┓┃┃┃┃┃•  ┣┫┓┏┓┓┏┓╋┏┓┏┓┏┳┓┏┓╋┓┏┏  ┃┃┏┓┏┓┓┏┓┏╋  ┃┃┃┏┓┏┓┏┓┏┓┏┓┏┓
         ┻┛┗┗┛┣┛┛ ┗•  ┻┛┗┗┛┗┛┗┛┗┛┛ ┛┗┗┗┻┗┗┗┛  ┣┛┛ ┗┛┃┗ ┗┗  ┛ ┗┗┻┛┗┗┻┗┫┗ ┛ 
        """)
    console.print(f"[bold cyan]{header}[/bold cyan]")
    console.print(
        "[bold green]Purpose:[/bold green] Project Manager tool for Bioinformaticians"
    )
    console.print("[bold green]Developer:[/bold green] Jyotirmoy Das")
    console.print("[bold green]Maintainer:[/bold green] Jyotirmoy Das")
    console.print("[bold green]Version:[/bold green] 0.1.0\n")

    author_name = smart_prompt("Enter your full name (First and Last Name)")

    while True:
        project_name = smart_prompt("Enter the project directory name")
        project_dir = Path.cwd() / project_name

        if project_dir.exists():
            overwrite = smart_confirm(f"{project_name} already exists. Overwrite?")
            if overwrite:
                shutil.rmtree(project_dir)
                console.print(
                    f"[bold yellow]Existing directory {project_name} removed.[/bold yellow]"
                )
                break
            else:
                console.print("Please enter a new project directory name.")
        else:
            break

    project_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"Created main directory: [bold cyan]{project_dir}[/bold cyan]")

    bfxpm_dir = project_dir / ".bfxpm"
    bfxpm_dir.mkdir()

    folders = [
        "scripts",
        "scripts/nextflow",
        "scripts/snakemake",
        "scripts/docker",
        "data/meta",
        "data/raw_external",
        "data/raw_internal",
        "doc",
        "intermediate",
        "logs",
        "notebooks",
        "results/figures",
        "results/reports",
        "results/tables",
        "scratch",
    ]

    for folder in folders:
        folder_path = project_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)

    log_file = project_dir / "logs" / "logs.qmd"
    log_file.touch()

    project_config = {
        "project_name": project_name,
        "author": author_name,
        "version": "0.1.0",
        "description": "A new bioinformatics project.",
    }
    with open(project_dir / "project.yml", "w") as f:
        yaml.dump(project_config, f, sort_keys=False)

    # --- MkDocs Scaffolding ---
    init_mkdocs = smart_confirm("Do you want to initialize MkDocs for this project?")
    if init_mkdocs:
        mkdocs_asset_dir = Path(__file__).parent.parent / "assets" / "mkdocs"
        if mkdocs_asset_dir.exists():
            # Copy mkdocs.yml
            shutil.copy(mkdocs_asset_dir / "mkdocs.yml", project_dir / "mkdocs.yml")
            # Create docs/ folder
            docs_dir = project_dir / "docs"
            docs_dir.mkdir(exist_ok=True)
            # Copy all markdown templates
            for md_file in (mkdocs_asset_dir / "docs").glob("*.md"):
                shutil.copy(md_file, docs_dir / md_file.name)
            
            # Replace placeholders in mkdocs.yml and docs/*.md
            today = datetime.now().strftime('%Y-%m-%d')
            for p in project_dir.glob("mkdocs.yml"):
                text = p.read_text()
                text = text.replace("[PROJECT_NAME]", project_name)
                text = text.replace("[AUTHOR_NAME]", author_name)
                p.write_text(text)
            
            for p in docs_dir.glob("*.md"):
                text = p.read_text()
                text = text.replace("[PROJECT_NAME]", project_name)
                text = text.replace("[AUTHOR_NAME]", author_name)
                text = text.replace("[DATE]", today)
                p.write_text(text)
                
            console.print("[bold green]✔[/bold green] MkDocs documentation scaffolded in [bold cyan]docs/[/bold cyan].")
            
            # Add mkdocs-material to pyproject.toml if it exists in current project root
            # (Assuming we want to influence the project being initialized)
            # Actually, the user likely wants it in their global/installer environment or the project metadata.
            # We'll add a note in project.yml or try to update a local pyproject.toml if the user creates one.
            # For now, let's just make sure the user knows they need mkdocs-material.
            console.print("[bold yellow]Tip:[/bold yellow] Install with 'pip install mkdocs-material' to build the site.")

    # --- Git Scaffolding ---
    init_git = smart_confirm(
        "Do you want to initialize a Git repository for this project?"
    )
    if init_git:
        github_user = smart_prompt("Enter your GitHub username (e.g. JD2112)")
        orcid_id = smart_prompt("Enter your ORCID ID (e.g. 0000-0000-0000-0000)", default="0000-0000-0000-0000")

        ignore_content = "# Ignore unnecessary files\n*.log\n*.tmp\n*.DS_Store\n__pycache__/\n.bfxpm/\ndata/\nresults/\nintermediate/\nscratch/\n"
        # If mkdocs was initialized, we might want to keep the documentation
        with open(project_dir / ".gitignore", "w") as f:
            f.write(ignore_content)

        # Asset based scaffolding
        asset_dir = Path(__file__).parent.parent / "assets" / "git-essentials"
        if asset_dir.exists():
            root_files = [
                ("CONTRIBUTION/CONTRIBUTING.md", "CONTRIBUTING.md"),
                ("CODE_OF_CONDUCT.md", "CODE_OF_CONDUCT.md"),
                ("LICENSE", "LICENSE"),
                ("CITATION.cff", "CITATION.cff"),
                ("CODEOWNERS.md", "CODEOWNERS.md"),
                ("SECURITY.md", "SECURITY.md"),
                ("SUPPORT.md", "SUPPORT.md"),
            ]
            
            for src_name, dest_name in root_files:
                src_path = asset_dir / src_name
                if src_path.exists():
                    shutil.copy(src_path, project_dir / dest_name)
                    
            if (asset_dir / ".gitattributes").exists():
                shutil.copy(asset_dir / ".gitattributes", project_dir / ".gitattributes")
            else:
                with open(project_dir / ".gitattributes", "w") as f:
                    f.write("* text=auto\n*.csv linguist-language=CSV\n")
 
            gh_dir = project_dir / ".github"
            gh_dir.mkdir(exist_ok=True)
            
            if (asset_dir / "ISSUE_TEMPLATE").exists():
                shutil.copytree(asset_dir / "ISSUE_TEMPLATE", gh_dir / "ISSUE_TEMPLATE", dirs_exist_ok=True)
                
            if (asset_dir / "workflows").exists():
                shutil.copytree(asset_dir / "workflows", gh_dir / "workflows", dirs_exist_ok=True)

            license_path = project_dir / "LICENSE"
            if license_path.exists():
                l_text = license_path.read_text()
                l_text = l_text.replace("[year]", str(datetime.now().year))
                l_text = l_text.replace("[fullname]", author_name)
                license_path.write_text(l_text)

            citation_path = project_dir / "CITATION.cff"
            if citation_path.exists():
                name_parts = author_name.split()
                given_name = name_parts[0] if name_parts else ""
                family_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                
                c_text = citation_path.read_text()
                c_text = c_text.replace("[FAMILY_NAME]", family_name)
                c_text = c_text.replace("[GIVEN_NAME]", given_name)
                c_text = c_text.replace("0000-0000-0000-0000", orcid_id)
                c_text = c_text.replace("[PROJECT_NAME]", project_name)
                c_text = c_text.replace("[DATE]", datetime.now().strftime('%Y-%m-%d'))
                citation_path.write_text(c_text)

            for p in project_dir.rglob("*"):
                if p.is_file():
                    try:
                        text = p.read_text(encoding="utf-8")
                        if "JD2112" in text:
                            p.write_text(text.replace("JD2112", github_user), encoding="utf-8")
                    except (UnicodeDecodeError, PermissionError):
                        pass
                
        try:
            is_new_repo = not (project_dir / ".git").exists()
            repo = Repo.init(project_dir)
            if is_new_repo:
                console.print(f"Git repository initialized in [bold cyan]{project_dir}[/bold cyan].")
            console.print(f"[bold green]✔[/bold green] Setup successful, template files copied from git-essentials.")
        except Exception as e:
            console.print(f"[bold red]Failed to initialize git repository: {e}[/bold red]")
    else:
        console.print(f"[bold green]✔[/bold green] Setup successful.")
    
    console.print(f"Run [bold cyan]bfxpm scan[/bold cyan] to view your files, then [bold cyan]bfxpm organize[/bold cyan] to sort them into [bold cyan]{project_name}[/bold cyan].")
