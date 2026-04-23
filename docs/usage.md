---
hide:
  - navigation
---

# Usage Guide

## Prerequisites
1. **Python**: Ensure you have Python 3.8 or higher installed.
2. **Dependencies**: The required libraries (`typer`, `rich`, `gitpython`, `pyyaml`) are managed via your package manager.
3. **External Tools**: For full functionality of `bfxpm fetch`, ensure specialized tools like the SRA Toolkit (`fastq-dump`) are in your system PATH.

## Detailed Workflow

### 1. Project Initialization
The `bfxpm init` command is your first step. It sets up a standard, industry-compliant directory structure that separates raw data from code and results.

```bash
bfxpm init
```

**Key Steps during Init:**

- **Author Information**: Used to populate `project.yml`, `LICENSE`, and `CITATION.cff`.
- **Git Initialization**: If you opt for Git, BfxPM will scaffold a comprehensive repository including:
    - **Governance**: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`.
    - **Visibility**: `SECURITY.md`, `SUPPORT.md`.
    - **Templates**: GitHub Issue and Pull Request templates in `.github/`.
    - **CI/CD**: Boilerplate GitHub Actions for CI and Versioning.
- **ORCID ID**: If Git is enabled, BfxPM asks for your *ORCID ID* to ensure proper scientific attribution in your `CITATION.cff`.

### 2. Analytical Scaffolding
BfxPM helps you transition from project setup to analysis by generating standard config and pipeline files.

#### Environment Management
Use `bfxpm env` to manage reproducible computing environments.

- `bfxpm env init`: Creates a standard Conda `environment.yml` with essential bioinfo channels (`bioconda`, `conda-forge`).
- `bfxpm env docker`: Generates a `Dockerfile` optimized for bioinformatics data.
- `bfxpm env singularity`: Generates a `Singularity.def` file for HPC compatibility.

#### Pipeline Scaffolding
Quickly drop pipeline templates into your project.

- `bfxpm pipeline snakemake`: Scaffold a `Snakefile` in `scripts/snakemake/`.
- `bfxpm pipeline nextflow`: Scaffold a `main.nf` in `scripts/nextflow/`.

### 3. Data Acquisition and Hygiene
BfxPM simplifies the messy process of downloading and managing large biological datasets.

#### Fetching Data
Use `bfxpm fetch` to pull data directly into `data/raw_external/`.
```bash
bfxpm fetch sra SRR123456
```
BfxPM automatically checks for dependencies and routes the output to ensure your project root stays clean.

#### Cleaning and Compression
Bioinformatics generates massive intermediate files. `bfxpm clean` helps you find and manage them.

- **Batch Compression**: Identifies uncompressed biological formats (`.fastq`, `.fast5`, `.pod5`, `.hifi`) and applies standardized lossless compression.
  - **Standard**: Converts to `.tar.gz`.
  - **Genomic**: Leverages `samtools` to convert BAM to CRAM and `pod5-utils` to convert FAST5 to POD5.
- **Large Data Sync**: While Git handles your code, `bfxpm sync --data` uses `rsync` to securely back up your massive `data/` directory to a cluster or remote server.
- **Archiving**: Moves entire directories to `archive/` to keep your active project view focused.

See the [References](references.md) section for more details on these compression formats.

???+ info "Compression Modes"
    `bfxpm clean compress` features a smarter, type-aware processing engine:

    *   **Mode Awareness**: You can run `bfxpm clean compress --mode genomic` to prioritize scientific formats, or keep it on `best` (default) to let BfxPM decide.
    *   **BAM to CRAM**: If `samtools` is installed, BfxPM will offer to convert your heavy BAM files to **CRAM**, saving 30-50% disk space while remaining 100% lossless.
    *   **FAST5 to POD5**: If `pod5-utils` is installed, it will offer to convert legacy Oxford Nanopore FAST5 files to the modern, more efficient **POD5** signal format.
    *   **Standard Fallback**: For all other formats (FASTQ, HiFi), it continues to provide standard `.tar.gz` compression to keep your project root clean.

    ```bash
    $ bfxpm clean --help
                                    
    Usage: bfxpm clean [OPTIONS] COMMAND [ARGS]...                                                                                              
    Manage and clean project disk space                                                                                                              
    ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                                                                          │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ temp        Find and prompt to delete large or intermediate files (*.sam, *.tmp).                                    │
    │ compress    Apply lossless compression to sequence and alignment files.                                              │
    │             Supports specialized formats like CRAM (for BAM) and POD5 (for FAST5).                                   │
    │ archive     Move an old folder into the project's archive/ directory.                                                │
    │ decompress  Decompress and restore files from .tar.gz, CRAM, or POD5 formats.                                        │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ```

    ```bash
    $ bfxpm clean compress --help

    Usage: bfxpm clean compress [OPTIONS]                                                                                                                                                                                                                      
    Apply lossless compression to sequence and alignment files. Supports specialized formats like CRAM (for BAM) and POD5 (for FAST5).  
                                                                                                                                        
    ╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --mode  -m      TEXT  Compression mode: 'standard' (tar.gz), 'genomic' (CRAM/POD5), or 'best' [default: best]                     │
    │ --keep                Don't delete original files after compression                                                               │
    │ --help                Show this message and exit.                                                                                 │
    ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

    ```

#### Restoring Documents (Decompress)
If you need to access archived or compressed files, use `bfxpm clean decompress`.

- **Restoration**: Automatically extracts `.tar.gz` and `.gz` files.
- **Genomic Reversion**:
  - **CRAM to BAM**: Restores your alignment files for tools that don't support CRAM.
  - **POD5 to FAST5**: Converts signal data back to legacy FAST5 format for older basecallers.

```bash
bfxpm clean decompress
```

### 4. Organization and Visualization
If your project gets messy, BfxPM's organization tools help you regain control.

- `bfxpm map`: Take a JSON snapshot of your current file locations before making changes.
- `bfxpm organize`: Iteratively route loose files to their designated BfxPM subfolders.
- `bfxpm tree`: View a beautiful, color-coded structure of your project in the terminal.

#### The Project "Time Machine"
BfxPM allows you to revert an organization attempt if you decide the previous layout was better.

1. **Snapshot**: Create a map *before* you organize: `bfxpm map`.
2. **Rollback**: To revert, provide the map file: use `-r` or `--rollback` flag followed by the map file name.
    ```bash
    bfxpm map --rollback bfxpm_structure_map_YYYYMMDD.json
    ```
3. BfxPM will locate your files and move them back to their original relative paths.

### 5. Reporting and Metadata
BfxPM automatically summarizes your project's status for publication or collaboration.
```bash
bfxpm report
```
This extracts your Git history, calculates file sizes, counts FASTQ samples, and generates a structured `PROJECT_SUMMARY.md`, `summary.json`, and `summary.yml`.

### 6. Data Integrity and Security
Bioinformatics data is fragile. **BfxPM** helps ensure your scientific results aren't based on corrupted files.

- `bfxpm checksum generate`: Creates a `checksums.md5` manifest for all files in `data/`.
- `bfxpm checksum verify`: Scans your data and compares it against the manifest to detect truncation or bit-rot.

### 7. Automated Flow Recording

#### Save terminal scripts to a file `bfxpm run_history`
When you run the right command after some troubles, and forget to save them, `bfxpm run_history` can scan your shell history and save them to a file.

???+ info "Run History"
    ```bash
    $ bfxpm run_history --help
    Usage: bfxpm run_history [OPTIONS]                                                                                                                                         
    Extract complex bioinformatics commands from shell history.                                                                                                                                          
    ╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ --save    --no-save      [default: no-save]                                                                                                     │
    │ --help                   Show this message and exit.                                                                                            │
    ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ```


#### `bfxpm flow`: Bridge the gap between interactive exploration and reproducible scripts.
    - `bfxpm flow start`: Starts monitoring your terminal interactions.
    - `bfxpm flow stop`: Automatically filters your shell history and saves your commands into a clean, reproducible `.sh` script in `scripts/`.

???+ info "Flow Recording"

    `bfxpm flow` and `bfxpm run_history` are designed to work in two completely different ways so that you're covered whether you planned ahead or not:

    1.  **`bfxpm run_history` (The "Oops" Tool)**:

        *   **No preparation needed.** It works even if you never ran `flow`. 
        *   It retrospectively scans your global shell history (e.g., the last 100 commands) and uses a filter to find complex bioinformatics calls (like `bwa`, `samtools`, `nextflow`) that you might have forgotten to document.
        *   It’s perfect for when you just finished a quick test and realized, "Wait, that command worked! How did I type it?"

    2.  **`bfxpm flow` (The "Pilot" Tool)**:

        *   **Requires `flow start`.** 
        *   It is a precise, time-bound session recorder. It only captures the commands you ran *during* a specific mission.
        *   It's perfect for when you're starting a formal analysis and want a clean, dedicated script of your exact workflow from start to finish.

    **In summary**: You do **not** need to run `flow` for `run_history` to work. `run_history` is a general search tool for your past, while `flow` is a high-fidelity recorder for your present! 

### 9. Project Portfolio Management
As you manage multiple research projects over time, BfxPM provides a way to index all your work into a unified portfolio.

- `bfxpm projects`: Scans your current root (e.g., your `projects/` or `lab/` folder) and identifies all standardized BfxPM projects.
- **HTML Export**: Use the `--html` flag to generate a professional `projects_index.html` file. This is a great way to maintain an interactive dashboard of your research progress, file counts, and activity dates.

```bash
bfxpm projects --html
```

---

```bash
$ bfxpm projects --help

Usage: bfxpm projects [OPTIONS] [PATH]

Scan and list all BfxPM projects in the given directory.

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   path      [PATH]  Root directory to scan for projects [default: .]                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --html                     Generate an HTML summary of all projects                                                        │
│ --help                     Show this message and exit.                                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### 10. Data Deposition
When you're ready to publish, BfxPM helps you prepare and deposit your data to public repositories.

- `bfxpm deposit list`: View all supported repositories (Zenodo, FigShare, Dryad, Dataverse, etc.).
- `bfxpm deposit prepare`: Create a clean ZIP bundle excluding `.git`, `.venv`, and temp files. Use `--include-data` / `--include-results` flags to control what's included.
- `bfxpm deposit go zenodo`: Open the deposit page for a specific repository directly in your browser.

???+ info "Data Deposit List"

    Supported Repositories:
    
    - [Zenodo](https://zenodo.org/deposit) : Open repository for EU-funded research outputs from Horizon Europe, Euratom, and earlier Framework Programmes.
    - [Figshare](https://figshare.com/account/home): Figshare is a provider of repository infrastructure. Our solutions help organizations and researchers share, showcase and manage their outputs.
    - [Dataverse](https://dataverse.org/): The Dataverse Project is an open-source software for sharing, preserving, citing, exploring, and analyzing research data.
    - [Dryad](https://datadryad.org/stash): Dryad is a curated resource that makes the data underlying scientific and medical literature discoverable and reusable.
    - [Mendeley](https://data.mendeley.com/): Mendeley is a reference manager and academic social network.
    - [Datahub](https://datahub.io/): Datahub is a data catalog for the modern data stack.
    - [Dans](https://dans.knaw.nl/en/): DANS is a Dutch institute for research data.
    - [Eudat](https://eudat.eu/services/b2share): EUDAT provides data management services for researchers in Europe.


???+ warning "Data Deposit Guard"

    - In `bfxpm deposit go`, before opening a repository's website (like Zenodo or FigShare), a **📂 Data Deposit Alert** is now shown.
    - The tool intelligently labels the repository as either **"EU-based"** (e.g., Zenodo, DANS, EUDAT) or **"Outside the EU"** based on its primary service location.
    - It requires a final confirmation to ensure the user has reviewed the data for sensitive information and residency compliance before the browser is opened.


```bash
# Prepare a publication-ready bundle
bfxpm deposit prepare --output my_project_v1.zip

# Open Zenodo deposit page
bfxpm deposit go zenodo
```

### 12. Agentic AI Support

BfxPM includes a project-aware **BioAssistant** to help you navigate your research and automate management tasks.

- **Setup**: `bfxpm ai setup` to connect to Gemini or Ollama.
- **Consulting**: Use `bfxpm ai chat` for an interactive session where the agent can see your file tree and help you organize your work.
- **Automation**: Ask the agent to perform tasks like *"Clean up all empty directories in my results folder"*. BfxPM's **Safety Interceptor** ensures no destructive commands are run without confirmation and backup.

For more details, see the dedicated [AI Agent](ai_agent.md) page.

### 11. Help

```bash
$ bfxpm --help
                                                                                                                                                   
 Usage: bfxpm [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                                                                                                                                                              
 #=================================================# 
 #   BfxPM: Bioinformatician's Project Manager         #                                           
 #=================================================#                                                                         
 Purpose: Project Manager tool for Bioinformaticians                                                                                               
 Developer: Jyotirmoy Das                                                                                                                          
 Maintainer: Jyotirmoy Das                                                                                                                         
 Version: 0.1.0                                                                                                                                    
                                                                                                                                                   
 Bioinformatician's Project Manager CLI                                                                                                                
                                                                                                                                                   
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                         │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                  │
│ --help                        Show this message and exit.                                                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ init         Initialize a new BfxPM project including folder structures and Git repository.                                                     │
│ scan         Scan a directory for files, summarizing extensions and disk usage.                                                                 │
│ organize     Organize scattered files and handle unknown directories into a BfxPM project.                                                      │
│ tree         Show a beautiful tree view of the directory and files.                                                                             │
│ projects     Scan and list all BfxPM projects in the given directory.                                                                           │
│ compress     Compress a large folder to tar.gz to save space.                                                                                   │
│ save         Save (version control) your scripts and config.                                                                                    │
│ history      View a beautiful timeline of script modifications with usage details.                                                              │
│ sync         Sync your project progress (Git) and optionally your large data folder (Rsync).                                                    │
│ login        Save GitHub/Cloud token locally.                                                                                                   │
│ logout       Remove locally saved credentials.                                                                                                  │
│ run_history  Extract complex bioinformatics commands from shell history.                                                                        │
│ show         Show all the hidden files in the project folder.                                                                                   │
│ report       Generate HTML/Markdown summary report and accompanying metadata files.                                                             │
│ update       Update BfxPM to the latest version via pip.                                                                                                               │
│ modify       Manually move any files or directories to a new location.                                                                          │
│ map          Create a map of the current directory structure OR rollback to a previous map.                                                     │
│ clean        Manage and clean project disk space                                                                                                │
│ env          Manage standard bioinformatics environments                                                                                        │
│ pipeline     Scaffold analysis pipelines                                                                                                        │
│ fetch        Fetch and route external biological data                                                                                           │
│ checksum     Manage data integrity using checksums                                                                                              │
│ flow         Record terminal sessions into scripts                                                                                              │
│ deposit      Deposit project data to public repositories                                                                        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


```