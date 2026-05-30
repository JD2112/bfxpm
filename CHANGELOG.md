# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-04-23

### Changed
- **Metadata Alignment**: Synchronized the package version `1.0.1` consistently across `pyproject.toml`, `src/bfxpm/__init__.py`, and `conda/meta.yaml`.
- **Conda Recipe**: Fixed YAML escaping/quoting syntax for the project summary definition in `conda/meta.yaml`.

## [1.0.0] - 2026-04-23

### Added
- **Interactive Scaffolding & Command Center**:
  - Built-in `init` command to bootstrap gold-standard, FAIR-compliant project structures with license, metadata, and gitignore.
  - Built-in `organize` tool to classify and route raw biological data, results, reports, scripts, and logs.
  - Multi-command ecosystem including `tree`, `projects`, `compress`, `save`, `history`, `sync`, `login`, `logout`, `run_history`, `show`, `report`, `update`, `modify`, and `map`.
- **Specialized Bioinformatics Tools**:
  - `clean`: Manage and reclaim disk space from large, temporary bioinformatics files.
  - `env`: Orchestrate standard bioinformatics stacks and environment profiles.
  - `pipeline`: Bootstrap Snakemake or Nextflow workflows instantly.
  - `fetch`: Retrieve and route dataset files directly from major external biological repositories.
  - `checksum`: Protect massive datasets from silent bit-rot with full automated manifest management.
  - `flow`: Trace and record interactive terminal sessions into clean, reproducible scripts.
  - `deposit`: Compile and package metadata packages for seamless deposition into FigShare, Dryad, or Zenodo.
- **Agentic AI BioAssistant Integration**:
  - Powered by Hugging Face `smolagents` and the `google-genai` SDK.
  - Provides a project-aware chatbot (`bfxpm ai chat`) which understands the active project structure and files.
  - Displays transparent real-time "Internal Thoughts" reasoning chains.
  - Support for local LLMs via `Ollama` and remote models via `google-genai`.
- **Intelligent Safety Layer**:
  - Safety interceptor that detects potentially destructive operations (e.g., `rm`).
  - Automated timestamped backups of target paths within `.bfxpm/backups/`.
  - Rich-rendered interactive confirmation prompts.
- **Testing & Quality Assurance**:
  - Robust `pytest` harness testing CLI initialization, outside-in vacuums, scans, and summary report generations.
