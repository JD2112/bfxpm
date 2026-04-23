import typer
import shutil
from datetime import datetime
from pathlib import Path
from bfxpm.utils import console, get_project_dir, smart_prompt, smart_confirm


def organize(
    path: str = typer.Argument(".", help="Directory containing messy files"),
    recursive: bool = typer.Option(
        True, "--recursive", "-r", help="Organize files recursively"
    ),
):
    """Organize scattered files and handle unknown directories into a BfxPM project."""
    source_dir = Path(path).resolve()
    if not source_dir.exists():
        console.print(f"[bold red]Path {source_dir} does not exist.[/bold red]")
        return

    target_root = get_project_dir()
    curr_cwd = Path.cwd()

    standard_folders = {
        "scripts",
        "data",
        "doc",
        "intermediate",
        "logs",
        "notebooks",
        "results",
        "scratch",
    }

    mappings = {
        # Scripts & Notebooks
        ".py": "scripts",
        ".python": "scripts",
        ".r": "scripts",
        ".sh": "scripts",
        ".bash": "scripts",
        ".ksh": "scripts",
        ".csh": "scripts",
        ".zsh": "scripts",
        ".c": "scripts",
        ".cpp": "scripts",
        ".h": "scripts",
        ".hpp": "scripts",
        ".java": "scripts",
        ".cs": "scripts",
        ".go": "scripts",
        ".rs": "scripts",
        ".swift": "scripts",
        ".kt": "scripts",
        ".kts": "scripts",
        ".dart": "scripts",
        ".php": "scripts",
        ".rb": "scripts",
        ".lua": "scripts",
        ".pl": "scripts",
        ".awk": "scripts",
        ".yml": "scripts",
        ".yaml": "scripts",
        ".json": "scripts",
        ".toml": "scripts",
        ".ipynb": "notebooks",
        ".rmd": "notebooks",
        ".qmd": "notebooks",
        # Genomic Data - Raw
        ".fastq": "data/raw_external",
        ".fq": "data/raw_external",
        ".fasta": "data/raw_external",
        ".fa": "data/raw_external",
        ".hifi": "data/raw_external",
        ".fast5": "data/raw_external",
        ".pod5": "data/raw_external",
        # Genomic Data - Processed/Alignment/Variation
        ".bam": "data/raw_internal",
        ".sam": "data/raw_internal",
        ".cram": "data/raw_internal",
        ".vcf": "data/raw_internal",
        ".bcf": "data/raw_internal",
        ".bed": "data/raw_internal",
        ".gff": "data/raw_internal",
        ".gtf": "data/raw_internal",
        # Indices
        ".fai": "data/raw_internal",
        ".bai": "data/raw_internal",
        ".csi": "data/raw_internal",
        ".tbi": "data/raw_internal",
        ".dict": "data/raw_internal",
        # Archives & Compressed (Fallback)
        ".gz": "data/raw_external",
        ".zip": "data/raw_external",
        ".tar": "data/raw_external",
        ".bz2": "data/raw_external",
        # R / Analysis Data
        ".rdata": "intermediate",
        ".rda": "intermediate",
        ".rds": "intermediate",
        ".rdb": "intermediate",
        # Visuals
        ".png": "results/figures",
        ".pdf": "results/figures",
        ".jpg": "results/figures",
        ".jpeg": "results/figures",
        ".html": "results/figures",
        ".svg": "results/figures",
        # Tables
        ".csv": "results/tables",
        ".tsv": "results/tables",
        ".xlsx": "results/tables",
        ".xls": "results/tables",
        # Docs & Logs
        ".md": "doc",
        ".txt": "doc",
        ".log": "logs",
        ".docx": "doc",
        # Workflows & Pipelines
        ".nf": "scripts/nextflow", ".nextflow": "scripts/nextflow", ".nextflow_config": "scripts/nextflow",
        ".smk": "scripts/snakemake", ".snakefile": "scripts/snakemake",
        # Containers
        ".sif": "intermediate", ".img": "intermediate", ".dockerfile": "scripts/docker",
        # Development & Config
        ".lock": "scripts", ".editorconfig": "scripts", ".gitignore": "scripts", ".gitattributes": "scripts", ".config": "scripts",
    }

    # Handle double extensions and special filenames without extensions
    def get_full_extension(p: Path):
        # Specific filename handling
        name_lower = p.name.lower()
        if name_lower == "nextflow.config":
            return ".nextflow_config"
        if name_lower in ["snakefile", "dockerfile", "makefile", "procfile"]:
            return "." + name_lower
            
        suffixes = p.suffixes
        if len(suffixes) >= 2:
            last_two = "".join(suffixes[-2:]).lower()
            if last_two in [
                ".fastq.gz",
                ".fq.gz",
                ".fasta.gz",
                ".fa.gz",
                ".tar.gz",
                ".vcf.gz",
            ]:
                return last_two
        return p.suffix.lower()

    protected_folders = set()
    if source_dir == target_root or target_root in source_dir.parents:
        protected_folders.update(standard_folders)

    for item in source_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            if (item / ".bfxpm").exists() or (item / "project.yml").exists():
                protected_folders.add(item.name)
                if item == target_root:
                    console.print(
                        f"[bold blue]Notice: Found project in subdirectory. Files will be organized into: [cyan]{target_root.name}[/cyan][/bold blue]"
                    )

    protected_files = {"project.yml", "README.md", "logs.qmd", ".gitignore"}

    moved_count = 0
    files_to_check = (
        list(source_dir.rglob("*")) if recursive else list(source_dir.iterdir())
    )

    all_target_options = [
        "scripts",
        "data/meta",
        "data/raw_external",
        "data/raw_internal",
        "intermediate",
        "doc",
        "logs",
        "notebooks",
        "results/figures",
        "results/reports",
        "results/tables",
        "scratch",
    ]

    for file_path in files_to_check:
        if file_path.is_file():
            rel_path = file_path.relative_to(source_dir)

            if any(part.startswith(".") for part in rel_path.parts):
                continue

            if any(part in protected_folders for part in rel_path.parts[:-1]):
                continue

            if len(rel_path.parts) == 1 and rel_path.name in protected_files:
                continue

            ext = get_full_extension(file_path)
            if ext in mappings:
                target_sub = mappings[ext]

                # Special Handling for Confusing/Report/Analysis files
                if any(
                    kw in file_path.name.lower()
                    for kw in ["report", "et al", "summary", "analysis"]
                ):
                    target_reports_dir = target_root / "results/reports"
                    if file_path.parent == target_reports_dir:
                        continue

                    console.print(
                        f"\n[bold yellow]Confusing file detected:[/bold yellow] [cyan]{file_path.name}[/cyan]"
                    )
                    console.print(f"Current location: [dim]{file_path.parent}[/dim]")
                    console.print("Where should this be moved?")

                    for i, opt in enumerate(all_target_options, 1):
                        console.print(f" [{i}] [bold cyan]{opt}[/bold cyan]")
                    console.print(" [s] [dim]Skip[/dim]")

                    choice = smart_prompt("Select destination", default="s")

                    if choice.lower() == "s":
                        console.print(f"[dim]Skipped {file_path.name}[/dim]")
                        continue

                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(all_target_options):
                            target_sub = all_target_options[idx]
                        else:
                            console.print(
                                f"[dim]Invalid choice, skipped {file_path.name}[/dim]"
                            )
                            continue
                    except ValueError:
                        console.print(
                            f"[dim]Invalid choice, skipped {file_path.name}[/dim]"
                        )
                        continue

                target_dir = target_root / target_sub

                if file_path.parent == target_dir:
                    continue

                target_dir.mkdir(parents=True, exist_ok=True)
                target_path = target_dir / file_path.name

                if target_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    target_path = (
                        target_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"
                    )

                shutil.move(str(file_path), str(target_path))
                console.print(f"[dim]Moved {rel_path} to {target_sub}[/dim]")
                moved_count += 1

    for item in source_dir.iterdir():
        if (
            item.is_dir()
            and not item.name.startswith(".")
            and item.name not in protected_folders
        ):
            is_empty = not any(item.iterdir())
            empty_msg = " (empty)" if is_empty else ""

            console.print(
                f"\n[bold yellow]Unknown directory detected:[/bold yellow] [cyan]{item.name}[/cyan]{empty_msg}"
            )

            default_action = "d" if is_empty else "s"
            action = smart_prompt(
                f"What should I do with '{item.name}'? (m: move to scratch, d: delete, s: skip)",
                default=default_action,
            )

            if action.lower() == "m":
                scratch_dir = target_root / "scratch"
                scratch_dir.mkdir(exist_ok=True)

                dest = scratch_dir / item.name
                if dest.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    dest = scratch_dir / f"{item.name}_{timestamp}"

                shutil.move(str(item), str(dest))
                console.print(f"[green]Moved '{item.name}' to scratch.[/green]")
            elif action.lower() == "d":
                if smart_confirm(
                    f"Are you sure you want to PERMANENTLY delete '{item.name}'?"
                ):
                    shutil.rmtree(item)
                    console.print(f"[red]Deleted '{item.name}'.[/red]")
            else:
                console.print(f"[dim]Skipped '{item.name}'.[/dim]")

    dest_msg = (
        f" into [bold cyan]{target_root.name}[/bold cyan]"
        if target_root != source_dir
        else ""
    )
    console.print(
        f"\n[bold green]✔ Organized {moved_count} files{dest_msg}.[/bold green]"
    )
    if target_root != source_dir:
        console.print(f"Check your folder: [bold cyan]{target_root.name}[/bold cyan]")

    dest_msg = (
        f" into [bold cyan]{target_root.name}[/bold cyan]"
        if target_root != source_dir
        else ""
    )
    console.print(
        f"\n[bold green]✔ Organized {moved_count} files{dest_msg}.[/bold green]"
    )
    if target_root != source_dir:
        console.print(f"Check your folder: [bold cyan]{target_root.name}[/bold cyan]")
