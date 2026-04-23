import os
from pathlib import Path
from smolagents import tool
from bfxpm.utils import get_project_dir

@tool
def list_project_files(recursive: bool = False) -> str:
    """
    Lists the files in the current bioinformatics project.
    Args:
        recursive: Whether to list files recursively.
    """
    root = get_project_dir()
    result = []
    if recursive:
        for r, _, f in os.walk(root):
            if any(x in r for x in [".git", ".venv", ".bfxpm"]):
                continue
            for file in f:
                result.append(os.path.join(r, file))
    else:
        result = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
    
    return "\n".join(result[:100]) or "No files found."

@tool
def read_metadata() -> str:
    """
    Reads the bioinformatics project metadata from project_tracker.yaml or pyproject.toml.
    """
    root = get_project_dir()
    for mf in ["project_tracker.yaml", "pyproject.toml", "project.yml"]:
        path = root / mf
        if path.exists():
            with open(path, "r") as f:
                return f"Content of {mf}:\n{f.read()}"
    return "No metadata file found."

@tool
def get_bfxpm_manual() -> str:
    """
    Returns a summary of available BfxPM commands and their purposes.
    """
    return """
    Available commands:
    - init: Initialize project
    - scan: Scan for files
    - organize: Route files to correct folders
    - clean: Manage disk space
    - checksum: Data integrity
    - flow: Record sessions
    - sync: Backup data
    - report: Project status
    """

# Tool Registry for smolagents
BIO_TOOLS = [list_project_files, read_metadata, get_bfxpm_manual]
