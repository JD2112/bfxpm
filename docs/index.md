---
hide:
  - navigation
  - toc
---

# Introduction

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/JD2112/bioinformatics_project_manager)](https://github.com/JD2112/bioinformatics_project_manager)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

<div class="grid-container" markdown="1">

<div class="main-content" markdown="1">

**BfxPM (Bioinformatician's Project Manager)** is an active command-line interface (CLI) manager designed specifically for the dynamic and often disorganized nature of computational biology research.

### Why BfxPM?

While general scaffolding tools (like [*Cookiecutter*](https://github.com/cookiecutter/cookiecutter)) excel at *Day 1 initialization*, they offer little support for the long-term maintenance of a project. BfxPM is designed to address the **"Day 365"** problem:

- **Ongoing Hygiene**: Route loose FASTQ, BAM, and script files that accumulate over time.
- **Scientific Attribution**: Automatic generation of `CITATION.cff` and `ORCID ID` integration ensuring you and your team get credit.
- **Reproducibility**: Integrated scaffolding for Conda, Docker, and Singularity from the start.
- **Resource Management**: Tools to identify and compress massive biological datasets that would otherwise deplete server storage.

### Installation

BfxPM is cross-platform and can be installed via the two primary scientific package managers:

**Via Pip:**
```bash
pip install bfxpm
```

**Via Conda (Bioconda):**
```bash
conda install jd2112::bfxpm
```

### Standard Alignment

BfxPM is built on the philosophy of global reproducibility standards. Our structures and workflows are aligned with:

- **The Turing Way**: The leading international handbook for reproducible data science.
- **ELIXIR & Software Carpentry**: Best practices for the separation of Raw Data from Mutable Scripts.
- **nf-core / Snakemake**: Industry-standard directory hierarchy for streamlined pipeline deployment.

## Core Capabilities

1. **Intelligent Initialization** (`bfxpm init`):
    - Sets up an industry-standard directory structure.
    - **Automatic Git Scaffolding**: Generates Open Source essentials (`LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff`) along with GitHub workflow boilerplates for CI and versioning.
2. **Dynamic Organization** (`bfxpm organize` / `bfxpm map` / `bfxpm modify`):
    - Iteratively route scattering FASTQs, scripts, and logs into their correct subfolders using smart rules.
3. **Environment & Pipeline Scaffolding** (`bfxpm env` / `bfxpm pipeline`):
    - Instantly spawn `environment.yml`, `Singularity.def`, `Snakefile` or `main.nf` templates directly into your project scripts.
4. **Data Acquisition** (`bfxpm fetch`):
    - Hook into SRA (via `fastq-dump`) to cleanly fetch and automatically route raw data into `data/raw_external/`.
5. **Project Hygiene** (`bfxpm clean` / `bfxpm compress`):
    - **Smart Clean**: Finds giant `*.sam` or `*.tmp` files.
    - **Smart Compress**: Scans specifically for biological formats (`.fastq`, `.fast5`, `.pod5`, `.hifi`) and batches them into `tar.gz` archives.
    - **Archive**: Move old datasets to a managed `archive/` directory.
6. **Reporting & Tracking** (`bfxpm report` / `bfxpm history`):
    - Generate human-readable summaries (`PROJECT_SUMMARY.md`) and machine-readable metadata (`.json`, `.yml`) accounting for project size, sample counts, and git history.
7. **Agentic AI Integration** (`bfxpm ai`):
    - **BioAssistant**: A project-aware AI agent that helps with organization, research questions, and automated management.
    - **Safety-First**: Integrated safety interceptors for destructive actions and support for local execution (Ollama).

## Quick Start

Initialize your scholarly project:
```bash
bfxpm init
```

Clean up and compress your sequence data:
```bash
bfxpm clean compress
```

Generate a detailed status report:
```bash
bfxpm report
```

For more details and further functionality, please refer to the [usage documentation](usage.md) and the [commands & parameters documentation](parameters.md).

## Credits
**BfxPM** was developed by **Jyotirmoy Das** to streamline active bioinformatics research and analysis. It integrates smoothly into High Performance Computing (HPC) environments using standard python tooling.

</div>

<div class="side-panel" markdown="1">

<p align="center">
  <img src="../assets/bfxpm_logo.png" width="200" alt="BfxPM Logo">
</p>

## Supported Ecosystems
[![](https://img.shields.io/badge/Typer-supported-black?logo=python)](https://typer.tiangolo.com/)
[![](https://img.shields.io/badge/Conda-supported-lightgrey?logo=anaconda)](https://docs.conda.io/)

## Included Sub-Systems
<div class="tag-section">
  <a href="#" target="_blank"><span>Project Scaffolding</span></a>
  <a href="#" target="_blank"><span>File Mapping</span></a>
  <a href="#" target="_blank"><span>Smart Compress</span></a>
  <a href="#" target="_blank"><span>Git Automation</span></a>
  <a href="#" target="_blank"><span>Tree Viz</span></a>
  <a href="#" target="_blank"><span>Reporting Core</span></a>
</div>

## Stats
<div class="stats-grid">
  <div class="stats-item"><span id="gh-stars" class="stats-value">--</span><span class="stats-label">stars</span></div>
  <div class="stats-item"><span id="gh-issues" class="stats-value">--</span><span class="stats-label">open issues</span></div>
  <div class="stats-item"><span id="gh-last-release" class="stats-value">--</span><span class="stats-label">last release</span></div>
  <div class="stats-item"><span id="gh-last-update" class="stats-value">--</span><span class="stats-label">last update</span></div>
</div>



## Contributors
<div id="gh-contributors" class="contrib-grid">
  <!-- Dynamically populated from GitHub API -->
</div>

## Get Help
- [GitHub Issues](https://github.com/JD2112/bfxpm/issues)

</div>

</div>
