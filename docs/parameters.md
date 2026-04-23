---
hide:
  - navigation
---

# Command Line

BfxPM uses the `Typer` library to provide a rich CLI experience. The syntax is universally:

`bfxpm [COMMAND] [OPTIONS]` or 

`bfxpm [GROUP] [COMMAND] [OPTIONS]`

## Main Commands

| Command | Description |
| :---: | :--- |
| `bfxpm init` | Initializes a new project. Prompts for author name and GitHub username. If Git is enabled, it asks for your ORCID ID and scaffolds Open Source governance files (`LICENSE`, `CITATION.cff`, etc.) with your specific attribution. |
| `bfxpm map` | Creates a JSON map of the current directory structure. Use `--rollback` or `-r` with a path to a map file to revert your files back to the structure recorded in that snapshot. |
| `bfxpm organize` | Automatically routes scattered files (like `.fastq` to `data/raw_external/` or `.py` to `scripts/`) and intelligently prompts you on unknown directories. |
| `bfxpm projects` | Scans a root directory for all BfxPM projects. Displays a table with names, authors, dates, and file counts. Use `--html` to generate a standalone web index of your research portfolio. |
| `bfxpm tree` | Outputs a visual, rich-text `tree` view of the current project directory. Use `--all` or `-a` to show hidden files (e.g. `.git`). |
| `bfxpm report` | Generates HTML/Markdown summary reports containing git history metrics, file usage stats, directory layouts, and dumps out accompanying ` summary.json` and ` summary.yml` metadata files. |
| `bfxpm save` | A wrapper to `git commit -a -m "BfxPM Autosave"` to easily snapshot current scripts and configs. |
| `bfxpm history` | Views a beautiful timeline of script modifications based on your Git history. |
| `bfxpm sync` | Syncs code (Git) and optionally data (Rsync). Use `--data` and `--remote [PATH]` for large data transfers. |
| `bfxpm modify` | Manually prompts you to safely move any arbitrary files or directories to a new project location. |
| `bfxpm scan` | Scans a directory for files, summarizing extensions and estimating disk usage. |
| `bfxpm run_history` | Scrapes your `~/.bash_history` and `~/.zsh_history` to extract complex executed bioinformatics commands and formats them for reproducibility. |
| `bfxpm show` | Shows all the hidden files (like `.json` internal caches) in the project folder. |
| `bfxpm ai` | Access the Agentic AI BioAssistant for project management and research help. |
| `bfxpm exit` | Safely terminate the BfxPM session with a status summary. Type `q`, `exit`, or `abort` at any prompt to cancel the setup process immediately. |

???+ options
    ```bash
    $ bfxpm tree --help 
                                                                                                                                        
    Usage: bfxpm tree [OPTIONS] [PATH]                                                                          
    Show a beautiful tree view of the directory and files.                                                                                                                              
    ╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │   path      [PATH]  Directory to show tree for [default: .]                                                                          │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --pager      --no-pager      Use a pager for the output [default: pager]                                                             │
    │ --all    -a                  Show hidden files and directories                                                                       │
    │ --icons                      Show emojis/icons                                                                                       │
    │ --help                       Show this message and exit.                                                                             │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


    ```

## Sub-Command Groups

BfxPM bundles specific domain functions into logical groups.

### `bfxpm clean` 
Manage and clean project disk space.

| Sub-command | Argument / Option | Description |
| :--- | :--- | :--- |
| `temp` | *None* | Automatically scans for `.sam` and `.tmp` files. Prompts before permanently deleting them. |
| `compress` | `--mode` | Lossless compression. `standard` (tar.gz), `genomic` (CRAM/POD5), or `best` (automatic). |
| `decompress` | `--keep` | Restores archives (`.tar.gz`, `.gz`) and specialized formats (CRAM to BAM, POD5 to FAST5). |
| `archive` | `[FOLDER_NAME]` | Moves an outdated or completed folder safely into an `archive/` internal silo to keep the root directory neat. |

### `bfxpm env`
Manage standard bioinformatics environments.

| Sub-command | Argument / Option | Description |
| :--- | :--- | :--- |
| `init` | *None* | Creates a boilerplate `environment.yml` for Conda / Micromamba environments. |
| `docker` | *None* | Creates a basic `Dockerfile` configured to ingest `environment.yml`. |
| `singularity`| *None* | Creates a `Singularity.def` (Apptainer) optimized for HPC workload encapsulations. |

### `bfxpm pipeline`
Scaffold analysis pipelines.

| Sub-command | Argument / Option | Description |
| :--- | :--- | :--- |
| `snakemake` | *None* | Drops a minimal, fully configured `Snakefile` template in `scripts/snakemake/`. |
| `nextflow`  | *None* | Drops a `main.nf` and `nextflow.config` scaffold into `scripts/nextflow/`. |

### `bfxpm fetch`
Fetch and route external biological data directly to designated endpoints.

| Sub-command | Argument / Option | Description |
| :--- | :--- | :--- |
| `sra` | `[SRR_ID]` | Leverages `fastq-dump` to download dataset splits directly into `data/raw_external/`. |
| `ensembl` | `[BUILD]` | (Placeholder) Wraps `curl/wget` to pull reference FASTA strings to `data/references/`. |

### `bfxpm checksum`
Manage data integrity using MD5 checksums.

| Sub-command | Argument / Option | Description |
| :--- | :--- | :--- |
| `generate` | *None* | Scans `data/` and creates a `checksums.md5` manifest. |
| `verify` | *None* | Verifies files against the manifest to detect corruption. |

### `bfxpm flow`
Record interactive terminal sessions into reproducible scripts.

| Sub-command | Argument / Option | Description |
| :--- | :--- | :--- |
| `start` | *None* | Begins monitoring shell history for new commands. |
| `stop` | `[NAME]` | Filters history and saves commands to a `.sh` script in `scripts/`. |

### `bfxpm deposit`
Prepare and deposit project data to public repositories.

| Sub-command | Argument / Option | Description |
| :--- | :--- | :--- |
| `list` | *None* | Lists all supported public data repositories (Zenodo, FigShare, Dryad, etc.) with their URLs. |
| `prepare` | `--output`, `--include-data`, `--include-results` | Creates a clean ZIP bundle of the project for deposition, excluding `.git`, `.venv`, and temporary files. |
| `go` | `[REPO_NAME]` | Opens the deposit page for the chosen repository (e.g., `zenodo`, `figshare`) directly in your browser. |

### `bfxpm ai`
Agentic AI for bioinformatics project management.

| Sub-command | Argument / Option | Description |
| :--- | :--- | :--- |
| `setup` | *None* | Interactive setup for AI providers (Gemini, Ollama), models, and API keys. |
| `ask` | `[QUERY]` | Send a single question to the BioAssistant and get an immediate response. |
| `chat` | *None* | Enter an interactive, project-aware chat session with the BioAssistant. |
