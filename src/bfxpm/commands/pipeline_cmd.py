import typer
from pathlib import Path
from bfxpm.utils import console, get_project_dir

pipeline_app = typer.Typer(help="Scaffold analysis pipelines")

@pipeline_app.command("snakemake")
def pipeline_snakemake():
    """Drop a standardized Snakefile into scripts/snakemake/."""
    d = get_project_dir()
    smk_dir = d / "scripts" / "snakemake"
    smk_dir.mkdir(parents=True, exist_ok=True)
    snakefile = smk_dir / "Snakefile"
    
    content = """# Snakemake pipeline template
configfile: "config/config.yaml"

rule all:
    input:
        "results/final_output.txt"

rule example_rule:
    input:
        "data/raw_external/sample.fastq.gz"
    output:
        "results/alignment/sample.bam"
    shell:
        "echo 'Running alignment on {input}' > {output}"
"""
    with open(snakefile, "w") as f:
        f.write(content)
        
    console.print(f"[bold green]✔ Generated standard Snakefile at {snakefile.relative_to(d)}[/bold green]")

@pipeline_app.command("nextflow")
def pipeline_nextflow():
    """Drop standard nextflow files into scripts/nextflow/."""
    d = get_project_dir()
    nf_dir = d / "scripts" / "nextflow"
    nf_dir.mkdir(parents=True, exist_ok=True)
    main_nf = nf_dir / "main.nf"
    nf_config = nf_dir / "nextflow.config"
    
    main_content = """// Nextflow pipeline template
params.input = "data/raw_external/*.fastq.gz"
params.outdir = "results"

process exampleProcess {
    publishDir "${params.outdir}", mode: 'copy'

    input:
    path reads

    output:
    path "output.txt"

    script:
    \"\"\"
    echo "Processing ${reads}" > output.txt
    \"\"\"
}

workflow {
    reads_ch = Channel.fromPath(params.input)
    exampleProcess(reads_ch)
}
"""
    with open(main_nf, "w") as f:
        f.write(main_content)
        
    config_content = """// Nextflow config
params {
    cpus = 2
    memory = 4.GB
}
"""
    with open(nf_config, "w") as f:
        f.write(config_content)
        
    console.print(f"[bold green]✔ Generated main.nf and nextflow.config at {nf_dir.relative_to(d)}[/bold green]")
