import typer
from pathlib import Path
from bfxpm.utils import console, get_project_dir

env_app = typer.Typer(help="Manage standard bioinformatics environments")

@env_app.command("init")
def env_init():
    """Generate a standard environment.yml for Conda/Mamba."""
    d = get_project_dir()
    env_file = d / "config" / "environment.yml"
    
    if not env_file.parent.exists():
        env_file.parent.mkdir(parents=True)
        
    content = f"""name: {d.name}_env
channels:
  - conda-forge
  - bioconda
  - defaults
dependencies:
  - python=3.10
  - snakemake
  - fastqc
  - multiqc
  # Add other dependencies here
"""
    with open(env_file, "w") as f:
        f.write(content)
        
    console.print(f"[bold green]✔ Generated standard environment.yml at {env_file.relative_to(d)}[/bold green]")

@env_app.command("docker")
def env_docker():
    """Generate a standard Dockerfile."""
    d = get_project_dir()
    dockerfile = d / "Dockerfile"
    
    content = """FROM mambaorg/micromamba:latest

COPY config/environment.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml && \\
    micromamba clean --all --yes

WORKDIR /project
"""
    with open(dockerfile, "w") as f:
        f.write(content)
        
    console.print(f"[bold green]✔ Generated Dockerfile at {dockerfile.relative_to(d)}[/bold green]")

@env_app.command("singularity")
def env_singularity():
    """Generate a standard Singularity/Apptainer definition file."""
    d = get_project_dir()
    singularity_file = d / "Singularity.def"
    
    content = """Bootstrap: docker
From: mambaorg/micromamba:latest

%files
    config/environment.yml /tmp/environment.yml

%post
    micromamba install -y -n base -f /tmp/environment.yml
    micromamba clean --all --yes
    mkdir -p /project

%environment
    export PATH=/opt/conda/bin:$PATH

%runscript
    echo "Bioinformatics Environment Initialized"
"""
    with open(singularity_file, "w") as f:
        f.write(content)
        
    console.print(f"[bold green]✔ Generated Singularity.def at {singularity_file.relative_to(d)}[/bold green]")
