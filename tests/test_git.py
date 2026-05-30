import pytest
import re
from pathlib import Path
from unittest.mock import MagicMock, patch
from bfxpm.commands.git_cmds import get_current_version, COMMIT_TYPES

def test_get_current_version(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    
    # 1. Test version reading when file exists
    pyproject.write_text('[project]\nversion = "1.2.3"\n')
    assert get_current_version(tmp_path) == "1.2.3"
    
    # 2. Test fallback when file does not exist
    non_existent = tmp_path / "does_not_exist"
    assert get_current_version(non_existent) == "1.0.1"

def test_commit_types_defined():
    # Verify commit types exist
    types = [t[0] for t in COMMIT_TYPES]
    assert "feat" in types
    assert "fix" in types
    assert "docs" in types
    assert "chore" in types

@patch("bfxpm.commands.git_cmds.Repo")
@patch("bfxpm.commands.git_cmds.get_project_dir")
def test_bump_no_commits(mock_get_dir, mock_repo_class, tmp_path):
    mock_get_dir.return_value = tmp_path
    
    # Setup pyproject.toml
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nversion = "1.0.1"\n')
    
    # Mock Repo instances
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo
    mock_repo.tags = []
    mock_repo.iter_commits.return_value = [] # No commits
    
    from bfxpm.commands.git_cmds import bump
    from typer.testing import CliRunner
    from bfxpm.main import app
    
    runner = CliRunner()
    result = runner.invoke(app, ["bump"])
    assert result.exit_code == 0
    assert "No new commits found" in result.stdout

@patch("bfxpm.commands.git_cmds.Repo")
@patch("bfxpm.commands.git_cmds.get_project_dir")
def test_sync_sensitive_files_warning(mock_get_dir, mock_repo_class, tmp_path):
    mock_get_dir.return_value = tmp_path
    
    # Create an untracked .env file in temp folder
    env_file = tmp_path / ".env"
    env_file.touch()
    
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo
    mock_repo.untracked_files = [".env"]
    
    from typer.testing import CliRunner
    from bfxpm.main import app
    
    runner = CliRunner()
    result = runner.invoke(app, ["sync"])
    
    assert "WARNING: Untracked Sensitive Files Detected in Workspace" in result.stdout
