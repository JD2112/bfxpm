---
hide:
  - navigation
---

# Directory Structures

By shifting you towards a standardized framework, BfxPM aims to solve the "spaghetti data" problem. This documentation explains what output directories and logs BfxPM produces when running tools like `init`, `organize`, and `report`.

## Base Directory Structure

When running `bfxpm init`, the following standard directory tree is built (without git repo): 

???+ info "Base Directory Structure"
    See [bfxpm tree](#bfxpm-tree) for the directory structure with git repo.

```bash
My_Project/
├── .bfxpm/              # Internal BfxPM metadata
├── data/
│   ├── meta/            # Sample sheets, clinical metadata
│   ├── raw_external/    # Unmodified incoming sequences (FASTQ, FASTA)
│   └── raw_internal/    # Processed alignments and variants (BAM, VCF)
├── scripts/
│   ├── nextflow/        # Nextflow pipeline files (.nf, nextflow.config)
│   ├── snakemake/       # Snakemake pipeline files (Snakefile, .smk)
│   └── docker/          # Dockerfile definitions
├── doc/                 # Project documentation and manuscripts
├── intermediate/        # R objects, analysis intermediates
├── logs/                # Execution logs, SLURM outputs
│   └── logs.qmd         # Lab notebook / run log
├── notebooks/           # Jupyter, Quarto, R Markdown notebooks
├── results/
│   ├── figures/         # Output visualizations (PNG, SVG, PDF)
│   ├── reports/         # Summary reports (MultiQC, PROJECT_SUMMARY.md)
│   └── tables/          # Tabular outputs (CSV, TSV, XLSX)
├── scratch/             # Temporary workspace
├── project.yml          # Project metadata (name, author, version)
└── README.md
```

## Hidden Metadata Output

To safely orchestrate large file operations, BfxPM writes critical mapping dictionaries and history files.

### 1. Structure Maps
Created when running `bfxpm map` or when invoking an extensive `bfxpm organize`.

* **Where:** `bfxpm_structure_map_YYYYMMDD_HHMMSS.json` in the root dir.
* **What:** A JSON document cataloging the absolute path, size, and hash state of every single file *before* a structural migration begins. Used as a rollback snapshot.

### 2. Internal Cache
* **Where:** `.bfxpm/` hidden folder.
* **What:** Project initialization dates, user configuration, and developer tags injected dynamically by the `init` command.

## Summary Reports Output

When sharing computational projects with PIs or external teams, it's vital to show exactly the footprint and status of your work.

Invoking `bfxpm report` queries your Git log, counts the FASTQ samples, calculates Total GB footprints, and prints an output tree.

It generates these 3 files in **`results/reports/`**:

- **`PROJECT_SUMMARY.md`**: Human-readable markdown table and statistics summary.
- **`summary.json`**: Machine readable array objects for downstream programmatic integration.
- **`summary.yml`**: YAML version.

Additionally, **`bfxpm report`** automatically updates the **`README.md`** at the project root with the latest summary metrics, ensuring your project front-page always reflects the current data state.

**Example format:**
```json
{
    "generated_at": "2026-04-10 15:30:10.000",
    "project_name": "microbiome_2026",
    "metrics": {
        "num_fastqs": 24,
        "num_bams": 12,
        "total_size_gb": 450.20
    },
    "directories": [ "data/raw", "data/processed", "scripts" ],
    "recent_history": [
        { "date": "2026-04-09", "message": "Updated mapping logic." }
    ]
}
```

## Cleaning Subsystem Output

BfxPM does not randomly throw away data. Calling `bfxpm clean archive folder_name` generates:

* **Where:** `archive/folder_name/`
* **What:** It moves the old result folder away from active view, dropping it into the `archive` silo, protecting it from accidental script modifications while getting it out of your `tree` visualizations.

## Git Scaffolding & Scientific Attribution

If you enable Git during `bfxpm init`, the following files are automatically generated and personalized based on your prompts:

| File | Purpose |
| :--- | :--- |
| `LICENSE` | An MIT License file updated with the current **Year** and your **Full Name**. |
| `CITATION.cff` | A citation metadata file containing your **Given/Family names**, **ORCID ID**, **Project Title**, and **Release Date**. This allows others to cite your work easily. |
| `CONTRIBUTING.md` | Standard guidelines for external contributors. |
| `CODE_OF_CONDUCT.md` | Standard community behavior guidelines. |
| `SECURITY.md` | Policy for reporting vulnerabilities. |
| `SUPPORT.md` | Instructions on how to get help with the project. |
| `.github/` | Contains specialized sub-directories for `ISSUE_TEMPLATE` and `workflows` (CI and Versioning). |
| `.gitignore` | Configured to ignore large data, results, and intermediate folders by default to keep your repo lean. |

## `bfxpm init`

???+ Initialization
    ```bash
    $ bfxpm init
    #=================================================#
    #   BfxPM: Bioinformatician's Project Manager         #
    #=================================================#
    Purpose: Project Manager tool for Bioinformaticians
    Developer: Jyotirmoy Das
    Maintainer: Jyotirmoy Das
    Version: 0.1.0

    Enter your full name (First and Last Name): Jyotirmoy Das
    Enter the project directory name: test007
    Created main directory: /Documents/bfxpm/test007
    Do you want to initialize a Git repository for this project? [y/N]: y
    Enter your GitHub username (e.g. JD2112): JD2112
    Enter your ORCID ID (e.g. 0000-0000-0000-0000) [0000-0000-0000-0000]: 
    Git repository initialized in .
    ✔ Setup successful, template files copied from git-essentials.
    Run bfxpm scan to view your files, then bfxpm organize to sort them into test007.
    ```

## `bfxpm scan`

???+ scan
    ```bash
    $ bfxpm scan
    File Extension Scanner: test007   
    ┏━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┓
    ┃ Extension    ┃ Count ┃ Size (MB) ┃
    ┡━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━┩
    │ .md          │     9 │      0.03 │
    │ .yml         │     4 │      0.00 │
    │ no_extension │     3 │      0.00 │
    │ .cff         │     1 │      0.00 │
    │ .qmd         │     1 │      0.00 │
    └──────────────┴───────┴───────────┘

    ```


## `bfxpm tree`

???+ folder_structure
    ```bash
    $ cd test007
    $ bfxpm tree -a

    test007/
    ┣━━ .bfxpm/
    ┣━━ .git/
    ┃   ┣━━ hooks/
    ┃   ┃   ┣━━ applypatch-msg.sample
    ┃   ┃   ┣━━ commit-msg.sample
    ┃   ┃   ┣━━ fsmonitor-watchman.sample
    ┃   ┃   ┣━━ post-update.sample
    ┃   ┃   ┣━━ pre-applypatch.sample
    ┃   ┃   ┣━━ pre-commit.sample
    ┃   ┃   ┣━━ pre-merge-commit.sample
    ┃   ┃   ┣━━ pre-push.sample
    ┃   ┃   ┣━━ pre-rebase.sample
    ┃   ┃   ┣━━ pre-receive.sample
    ┃   ┃   ┣━━ prepare-commit-msg.sample
    ┃   ┃   ┣━━ push-to-checkout.sample
    ┃   ┃   ┣━━ sendemail-validate.sample
    ┃   ┃   ┗━━ update.sample
    ┃   ┣━━ info/
    ┃   ┃   ┗━━ exclude
    ┃   ┣━━ objects/
    ┃   ┃   ┣━━ info/
    ┃   ┃   ┗━━ pack/
    ┃   ┣━━ refs/
    ┃   ┃   ┣━━ heads/
    ┃   ┃   ┗━━ tags/
    ┃   ┣━━ config
    ┃   ┣━━ description
    ┃   ┗━━ HEAD
    ┣━━ .github/
    ┃   ┣━━ ISSUE_TEMPLATE/
    ┃   ┃   ┣━━ bug_report.md
    ┃   ┃   ┣━━ custom.md
    ┃   ┃   ┗━━ feature_request.md
    ┃   ┗━━ workflows/
    ┃       ┣━━ docker-build.yml
    ┃       ┣━━ github-pages-deployment.yml
    ┃       ┗━━ shinyapps_deploy.yml
    ┣━━ scripts/
    ┃   ┣━━ docker/
    ┃   ┣━━ nextflow/
    ┃   ┗━━ snakemake/
    ┣━━ data/
    ┃   ┣━━ meta/
    ┃   ┣━━ raw_external/
    ┃   ┗━━ raw_internal/
    ┣━━ doc/
    ┣━━ intermediate/
    ┣━━ logs/
    ┃   ┗━━ logs.qmd
    ┣━━ notebooks/
    ┣━━ results/
    ┃   ┣━━ figures/
    ┃   ┣━━ reports/
    ┃   ┗━━ tables/
    ┣━━ scratch/
    ┣━━ .gitattributes
    ┣━━ .gitignore
    ┣━━ CITATION.cff
    ┣━━ CODE_OF_CONDUCT.md
    ┣━━ CODEOWNERS.md
    ┣━━ CONTRIBUTING.md
    ┣━━ LICENSE
    ┣━━ project.yml
    ┣━━ README.md
    ┣━━ SECURITY.md
    ┗━━ SUPPORT.md
    ```
    use `:q` to quit the viewer.