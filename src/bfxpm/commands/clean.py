import typer
import shutil
import tarfile
from pathlib import Path
from bfxpm.utils import console, get_project_dir

clean_app = typer.Typer(help="Manage and clean project disk space")

@clean_app.command("temp")
def clean_temp():
    """Find and prompt to delete large or intermediate files (*.sam, *.tmp)."""
    d = get_project_dir()
    targets = list(d.rglob("*.sam")) + list(d.rglob("*.tmp"))
    if not targets:
        console.print("[green]No heavy intermediate files found. You are clean![/green]")
        return
        
    console.print("[bold yellow]Found the following heavy intermediate files:[/bold yellow]")
    for t in targets:
        console.print(f"- {t.relative_to(d)} ({t.stat().st_size / (1024*1024):.2f} MB)")
        
    if typer.confirm("Delete these files to save space?"):
        for t in targets:
            t.unlink()
        console.print("[bold green]✔ Files deleted.[/bold green]")

@clean_app.command("compress")
def clean_compress(
    mode: str = typer.Option("best", "--mode", "-m", help="Compression mode: 'standard' (tar.gz), 'genomic' (CRAM/POD5), or 'best'"),
    keep_original: bool = typer.Option(False, "--keep", help="Don't delete original files after compression")
):
    """
    Apply lossless compression to sequence and alignment files.
    Supports specialized formats like CRAM (for BAM) and POD5 (for FAST5).
    """
    import subprocess
    d = get_project_dir()
    
    # 1. Gather Alignment files (BAM)
    bam_files = list(d.rglob("*.bam"))
    
    # 2. Gather Raw Signal files (FAST5)
    fast5_files = list(d.rglob("*.fast5"))
    
    # 3. Gather Standard Sequence files
    seq_files = []
    for ext in ["*.fastq", "*.hifi"]:
        seq_files.extend(list(d.rglob(ext)))

    total_targets = len(bam_files) + len(fast5_files) + len(seq_files)
    
    if total_targets == 0:
        console.print("[green]No uncompressed or legacy biological formats found.[/green]")
        return
        
    console.print(f"[bold yellow]Found {total_targets} files for lossless compression processing.[/bold yellow]")

    # --- BAM to CRAM Processing ---
    if bam_files and (mode in ["genomic", "best"]):
        if shutil.which("samtools"):
            if typer.confirm(f"Convert {len(bam_files)} BAM files to lossless CRAM? (Saves ~30-50% space)"):
                for bam in bam_files:
                    cram = bam.with_suffix(".cram")
                    console.print(f"[cyan]Samtools: Converting {bam.name} -> {cram.name}...[/cyan]")
                    # Lossless CRAM usually requires a reference, but 'samtools view -C' 
                    # can work or skip reference if not provided. To stay truly lossless 
                    # and portable, we run simple conversion.
                    try:
                        subprocess.run(["samtools", "view", "-C", "-o", str(cram), str(bam)], check=True)
                        if not keep_original: bam.unlink()
                    except subprocess.CalledProcessError as e:
                        console.print(f"[red]Error converting {bam.name}: {e}[/red]")
        else:
            console.print("[yellow]Samtools not found. Skipping BAM->CRAM conversion.[/yellow]")

    # --- FAST5 to POD5 Processing ---
    if fast5_files and (mode in ["genomic", "best"]):
        if shutil.which("pod5"):
            if typer.confirm(f"Convert {len(fast5_files)} FAST5 files to modern POD5?"):
                for f5 in fast5_files:
                    p5 = f5.with_suffix(".pod5")
                    console.print(f"[cyan]POD5: Converting {f5.name} -> {p5.name}...[/cyan]")
                    try:
                        subprocess.run(["pod5", "convert", "fast5", str(f5), "--output", str(p5)], check=True)
                        if not keep_original: f5.unlink()
                    except subprocess.CalledProcessError as e:
                        console.print(f"[red]Error converting {f5.name}: {e}[/red]")
        else:
            console.print("[yellow]pod5-utils not found. Skipping FAST5->POD5 conversion.[/yellow]")

    # --- Sequence File Compression (Standard Gzip/Tar) ---
    if seq_files:
        if typer.confirm(f"Compress {len(seq_files)} sequence files to .gz / .tar.gz?"):
            for t in seq_files:
                console.print(f"[cyan]Gzip: Compressing {t.name}...[/cyan]")
                out_file = t.with_suffix(t.suffix + ".tar.gz")
                try:
                    with tarfile.open(out_file, "w:gz") as tar:
                        tar.add(t, arcname=t.name)
                    if not keep_original: t.unlink()
                except Exception as e:
                    console.print(f"[red]Error compressing {t.name}: {e}[/red]")

    console.print("[bold green]✔ Compression processing complete.[/bold green]")

@clean_app.command("archive")
def clean_archive(folder: str = typer.Argument(..., help="Folder to archive within project.")):
    """Move an old folder into the project's archive/ directory."""
    d = get_project_dir()
    target_dir = d / folder
    archive_dir = d / "archive"
    
    if not target_dir.exists():
        console.print(f"[bold red]Folder {target_dir} does not exist.[/bold red]")
        return
        
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / target_dir.name
    
    if typer.confirm(f"Move folder '{folder}' to archive?"):
        shutil.move(str(target_dir), str(dest))
        console.print(f"[bold green]✔ Archived to {dest.relative_to(d)}[/bold green]")

@clean_app.command("decompress")
def clean_decompress(
    keep_compressed: bool = typer.Option(False, "--keep", help="Don't delete compressed files after extraction")
):
    """
    Decompress and restore files from .tar.gz, CRAM, or POD5 formats.
    """
    import subprocess
    d = get_project_dir()
    
    # 1. Gather Alignment files (CRAM)
    cram_files = list(d.rglob("*.cram"))
    
    # 2. Gather Modern Signal files (POD5)
    pod5_files = list(d.rglob("*.pod5"))
    
    # 3. Gather Compressed Archive files
    tar_gz_files = list(d.rglob("*.tar.gz"))
    gz_files = [f for f in d.rglob("*.gz") if not f.name.endswith(".tar.gz")]

    total_targets = len(cram_files) + len(pod5_files) + len(tar_gz_files) + len(gz_files)
    
    if total_targets == 0:
        console.print("[green]No compressed or specialized formats found to decompress.[/green]")
        return
        
    console.print(f"[bold yellow]Found {total_targets} files for decompression processing.[/bold yellow]")

    # --- CRAM to BAM Processing ---
    if cram_files:
        if shutil.which("samtools"):
            if typer.confirm(f"Convert {len(cram_files)} CRAM files back to BAM?"):
                for cram in cram_files:
                    bam = cram.with_suffix(".bam")
                    console.print(f"[cyan]Samtools: Converting {cram.name} -> {bam.name}...[/cyan]")
                    try:
                        subprocess.run(["samtools", "view", "-b", "-o", str(bam), str(cram)], check=True)
                        if not keep_compressed: cram.unlink()
                    except subprocess.CalledProcessError as e:
                        console.print(f"[red]Error converting {cram.name}: {e}[/red]")
        else:
            console.print("[yellow]Samtools not found. Cannot decompress CRAM files.[/yellow]")

    # --- POD5 to FAST5 Processing ---
    if pod5_files:
        if shutil.which("pod5"):
            if typer.confirm(f"Convert {len(pod5_files)} POD5 files back to FAST5?"):
                for p5 in pod5_files:
                    f5_dir = p5.with_suffix(".fast5_extracted")
                    console.print(f"[cyan]POD5: Converting {p5.name} to FAST5...[/cyan]")
                    try:
                        # POD5 to FAST5 usually outputs to a directory
                        subprocess.run(["pod5", "convert", "to-fast5", str(p5), "--output", str(f5_dir)], check=True)
                        console.print(f"[dim]FAST5 files extracted to {f5_dir.name}/[/dim]")
                        if not keep_compressed: p5.unlink()
                    except subprocess.CalledProcessError as e:
                        console.print(f"[red]Error converting {p5.name}: {e}[/red]")
        else:
            console.print("[yellow]pod5-utils not found. Cannot decompress POD5 files.[/yellow]")

    # --- Archive Extraction (tar.gz) ---
    if tar_gz_files:
        if typer.confirm(f"Extract {len(tar_gz_files)} .tar.gz archives?"):
            for t in tar_gz_files:
                console.print(f"[cyan]Extracting {t.name}...[/cyan]")
                try:
                    with tarfile.open(t, "r:gz") as tar:
                        tar.extractall(path=t.parent, filter='data')
                    if not keep_compressed: t.unlink()
                except Exception as e:
                    console.print(f"[red]Error extracting {t.name}: {e}[/red]")

    # --- Simple Gzip Extraction (gz) ---
    if gz_files:
        import gzip
        if typer.confirm(f"Decompress {len(gz_files)} .gz files?"):
            for g in gz_files:
                out_file = g.with_suffix("")
                console.print(f"[cyan]Gunzip: Decompressing {g.name}...[/cyan]")
                try:
                    with gzip.open(g, 'rb') as f_in:
                        with open(out_file, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    if not keep_compressed: g.unlink()
                except Exception as e:
                    console.print(f"[red]Error decompressing {g.name}: {e}[/red]")

    console.print("[bold green]✔ Decompression processing complete.[/bold green]")
