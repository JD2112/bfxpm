import shutil
import datetime
import os
from pathlib import Path
from typing import List, Union, Optional
from rich.prompt import Confirm
from bfxpm.utils import console
from bfxpm.ai_config import AIConfig

class SafetyLayer:
    def __init__(self, config: AIConfig):
        self.config = config
        self.backup_dir = config.backup_dir

    def _ensure_backup_dir(self):
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            # Add to gitignore if it exists
            gitignore = self.config.project_dir / ".gitignore"
            if gitignore.exists():
                with open(gitignore, "r") as f:
                    content = f.read()
                if ".bfxpm/backups" not in content:
                    with open(gitignore, "a") as f:
                        f.write("\n# BfxPM AI Backups\n.bfxpm/backups/\n")

    def create_backup(self, target_path: Union[str, Path]) -> Optional[Path]:
        """Creates a timestamped backup of the target file/directory."""
        self._ensure_backup_dir()
        path = Path(target_path)
        if not path.exists():
            return None

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{timestamp}_{path.name}"
        backup_path = self.backup_dir / backup_name

        try:
            if path.is_file():
                shutil.copy2(path, backup_path)
            else:
                shutil.copytree(path, backup_path)
            return backup_path
        except Exception as e:
            console.print(f"[bold red]Backup failed:[/bold red] {e}")
            return None

    def confirm_destructive_action(self, action_description: str, targets: List[Union[str, Path]]) -> bool:
        """Prompts the user for confirmation and creates backups before proceeding."""
        console.print(f"\n[bold yellow]⚠️  CAUTION:[/bold yellow] Agent wants to perform: [bold cyan]{action_description}[/bold cyan]")
        
        for target in targets:
            console.print(f"Target: [red]{target}[/red]")

        if not Confirm.ask("Do you want to proceed?"):
            console.print("[yellow]Action cancelled by user.[/yellow]")
            return False

        # Create backups
        if self.config.get_safety_settings().get("auto_backup", True):
            for target in targets:
                backup = self.create_backup(target)
                if backup:
                    console.print(f"[green]Backup created:[/green] {backup}")
        
        return True

    def is_destructive(self, command: str) -> bool:
        """Heuristic to check if a command string is destructive."""
        harmful_keywords = ["rm ", "truncate ", "shred ", "overwrite ", "> ", ">> "]
        return any(kw in command.lower() for kw in harmful_keywords)
