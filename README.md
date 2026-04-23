# BfxPM: Bioinformatician's Project Manager

<p align="center">
  <img src="https://raw.githubusercontent.com/JD2112/bfxpm/main/assets/bfxpm_logo.png" width="300" alt="BfxPM Logo">
</p>

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Conda](https://img.shields.io/badge/install%20with-conda-green.svg)](https://anaconda.org/bioconda/bfxpm)
[![Standards: FAIR](https://img.shields.io/badge/Standards-FAIR-orange.svg)](https://www.nature.com/articles/sdata201618)

**BfxPM** is a professional-grade CLI ecosystem designed for the high-throughput, data-heavy workflows of modern computational biology. It transforms messy research directories into standardized, FAIR-compliant project structures, while providing an Agentic AI layer to assist with complex bioinformatic tasks.


## 🚀 Key Features

### 📂 Professional Scaffolding
*   **FAIR Compliance**: Instantly scaffold projects with `CONTRIBUTING.md`, `CITATION.cff`, `LICENSE`, and standard GitHub Action workflows.
*   **MkDocs Ready**: One-command generation of a complete documentation suite (`docs/`, `mkdocs.yml`).
*   **Scientific Attribution**: Auto-populates metadata with your ORCID ID and project specifics.

### 🔄 Intelligent Organization & Mapping
*   **`bfxpm organize`**: A specialized detection engine that routes sequences, alignments, and reports (PDF/HTML) into dedicated subfolders (`results/reports` vs `results/figures`).
*   **Outside-In Vacuum**: Run organization from a parent folder to "vacuum" messy files into your project structure.
*   **`bfxpm map --rollback`**: Take immutable snapshots of your project state and revert instantly.

### 🧬 Bioinformatics Toolset
*   **`bfxpm env`**: Standardized environment management for common bioinformatic stacks.
*   **`bfxpm pipeline`**: Scaffold analysis pipelines specifically for **Nextflow** and **Snakemake**.
*   **`bfxpm fetch`**: Intelligent data retrieval and routing from external biological repositories.
*   **`bfxpm tree`**: A high-performance scientific tree viewer with pager support and hidden file toggles.

### 🛡️ Data Integrity & Publication
*   **`bfxpm checksum`**: Full manifest management to detect bit-rot in massive datasets.
*   **`bfxpm flow`**: Record interactive terminal sessions into reproducible shell scripts.
*   **`bfxpm deposit`**: One-command preparation for deposition to Zenodo, FigShare, and Dryad.


## 🤖 Agentic AI Integration
BfxPM now features a built-in **BioAssistant** powered by [SmolAgents](https://github.com/huggingface/smolagents) and the **Gemini 1.5 Pro/Flash** SDK.

*   **`bfxpm ai chat`**: Interactive, project-aware assistant that understands your directory structure and data types.
*   **Transparent Reasoning**: Real-time "Internal Thoughts" display shows the agent's logic before it acts.
*   **Safety Interceptor**: Automatically intercepts destructive commands (like `rm`), creates timestamped backups in `.bfxpm/backups/`, and requires manual confirmation.
*   **Local & Cloud Flexibility**: Configure via `bfxpm ai setup` to use either local (Ollama) or cloud models.


## 🛠️ Installation

### Prerequisites
*   Python 3.13+ (Recommended)
*   Conda (Optional, for `bfxpm env` features)

### via Pip
```bash
pip install bfxpm
```

### via Conda
```bash
conda install jd2112::bfxpm
```

---

## 📖 Quick Start

**1. Initialize a "Gold Standard" project:**
```bash
bfxpm init
```

**2. Interact with your BioAssistant:**
```bash
bfxpm ai setup  # Configure your API keys
bfxpm ai chat   # "How should I structure my differential expression analysis?"
```

**3. Clean up the "Mess":**
```bash
bfxpm organize  # Automatically routes files and asks about unknown folders
```

**4. Visualize & Document:**
```bash
bfxpm tree --all  # View all files including hidden .git/
bfxpm report      # Generate a comprehensive project status report
bfxpm exit        # Safely exit the BfxPM session
```

---

## 🏢 Architecture & Development

### Project Structure
BfxPM follows a modular, production-grade architecture:
- `src/bfxpm/agents/`: AI agent logic and safety interceptors.
- `src/bfxpm/commands/`: Individual CLI command modules.
- `scripts/publish.py`: One-touch interactive publishing to PyPI and Anaconda.

### Developer Environment
To set up for contributions:
```bash
git clone https://github.com/jyoda68/bfxpm.git
cd bfxpm
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

---

## 📄 License & Attribution
Licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
Developed and maintained by **Jyotirmoy Das**.

---

## Developer's Notes
- **Python 3.13 Upgrade**: Migrated to Python 3.13 to leverage the latest performance improvements and resolver features.
- **SDK Transition**: Switched to the `google-genai` unified SDK for more robust Gemini integrations.
- **Safety First**: Destructive command interception is now a core part of the codebase to prevent accidental data loss in large-scale bioinformatic projects.

---

_Developed with ❤️ for Bioinformaticians by a Bioinformatician_