import os
import pytest
from pathlib import Path
from typer.testing import CliRunner
from bfxpm.main import app

runner = CliRunner()

@pytest.fixture
def test_env(tmp_path):
    # Change current working directory to temporary path
    original_cwd = Path.cwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_cwd)

def test_init_creates_structure(test_env):
    # Pass inputs via the prompt
    result = runner.invoke(app, ["init"], input="Test Author\ntest_project\nn\n")
    assert result.exit_code == 0
    project_dir = test_env / "test_project"
    
    assert project_dir.exists()
    assert (project_dir / "scripts").exists()
    assert (project_dir / "data/meta").exists()
    assert (project_dir / "project.yml").exists()
    
def test_organize_command(test_env):
    # Setup dummy files
    (test_env / "script.py").touch()
    (test_env / "data.fastq").touch()
    (test_env / "plot.png").touch()
    
    result = runner.invoke(app, ["organize"])
    assert result.exit_code == 0
    
    assert (test_env / "scripts" / "script.py").exists()
    assert (test_env / "data/raw_external" / "data.fastq").exists()
    assert (test_env / "results/figures" / "plot.png").exists()
    
    # Original files should be gone
    assert not (test_env / "script.py").exists()

def test_scan_command(test_env):
    (test_env / "test.py").touch()
    result = runner.invoke(app, ["scan"])
    assert result.exit_code == 0
    assert ".py" in result.stdout

def test_report_command(test_env):
    # Run from inside the temporary env
    result = runner.invoke(app, ["report"])
    assert result.exit_code == 0
    # Note: BfxPM report generates PROJECT_SUMMARY.md
    assert (test_env / "results" / "reports" / "PROJECT_SUMMARY.md").exists()
