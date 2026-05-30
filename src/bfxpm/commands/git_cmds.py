import re
import datetime
import typer
from rich.table import Table
from rich.prompt import Prompt, Confirm
from git import Repo
from bfxpm.utils import console, get_project_dir

COMMIT_TYPES = [
    ("feat", "A new feature"),
    ("fix", "A bug fix"),
    ("docs", "Documentation only changes"),
    ("style", "Changes that do not affect the meaning of the code (white-space, formatting, etc)"),
    ("refactor", "A code change that neither fixes a bug nor adds a feature"),
    ("perf", "A code change that improves performance"),
    ("test", "Adding missing tests or correcting existing tests"),
    ("build", "Changes that affect the build system or external dependencies (example scopes: pip, conda)"),
    ("ci", "Changes to our CI configuration files and scripts"),
    ("chore", "Other changes that don't modify src or test files"),
    ("revert", "Reverts a previous commit")
]

def get_current_version(project_dir) -> str:
    pyproject = project_dir / "pyproject.toml"
    if pyproject.exists():
        with open(pyproject, "r") as f:
            content = f.read()
        match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        if match:
            return match.group(1)
    return "1.0.1"

def save(
    msg: str = typer.Argument(
        None, 
        help="Optional commit message. If omitted, triggers interactive Conventional Commit prompt."
    )
):
    """
    Save (version control) your scripts and config.
    
    This command acts as a wrapper around Git. It automatically tracks all new or modified 
    project files (like code, config, documentation). If a message is provided, it commits 
    immediately. Otherwise, it launches an interactive Commitizen-style prompter.
    """
    d = get_project_dir()
    try:
        repo = Repo(d)
        
        # Check if there are changes to commit
        if not repo.is_dirty(untracked_files=True):
            console.print("[yellow]No changes detected. Nothing to save.[/yellow]")
            return

        if msg is None:
            console.print("[bold cyan]Commitizen Interactive Commit Prompter[/bold cyan]")
            console.print("Select the type of change that you're committing:")
            for idx, (t, desc) in enumerate(COMMIT_TYPES, start=1):
                console.print(f"  [bold green]{idx}[/bold green]. [cyan]{t:<10}[/cyan] - {desc}")
            
            while True:
                choice = Prompt.ask("Choose a type (number or name)", default="1")
                chosen_type = None
                if choice.isdigit():
                    val = int(choice)
                    if 1 <= val <= len(COMMIT_TYPES):
                        chosen_type = COMMIT_TYPES[val - 1][0]
                else:
                    choice_clean = choice.strip().lower()
                    if choice_clean in [t[0] for t in COMMIT_TYPES]:
                        chosen_type = choice_clean
                
                if chosen_type:
                    break
                console.print("[bold red]Invalid selection. Please choose a valid type.[/bold red]")

            scope = Prompt.ask("What is the scope of this change? (e.g., pipeline, ai, deps) (press enter to skip)", default="").strip()
            subject = Prompt.ask("Write a short, imperative tense description of the change").strip()
            while not subject:
                subject = Prompt.ask("[bold red]Subject is required.[/bold red] Write a short description").strip()
                
            body = Prompt.ask("Provide a longer description of the change (press enter to skip)", default="").strip()
            
            is_breaking = Confirm.ask("Are there any breaking changes?", default=False)
            breaking_desc = ""
            if is_breaking:
                breaking_desc = Prompt.ask("Describe the breaking changes").strip()
                while not breaking_desc:
                    breaking_desc = Prompt.ask("[bold red]Breaking change description is required if yes.[/bold red] Describe the breaking changes").strip()

            closed_issues = Prompt.ask("Does this change close any open issues? (e.g., #31, #34) (press enter to skip)", default="").strip()

            # Build commit message
            scope_str = f"({scope})" if scope else ""
            breaking_marker = "!" if is_breaking else ""
            
            commit_msg = f"{chosen_type}{scope_str}{breaking_marker}: {subject}"
            
            body_parts = []
            if body:
                body_parts.append(body)
            if is_breaking:
                body_parts.append(f"BREAKING CHANGE: {breaking_desc}")
            if closed_issues:
                body_parts.append(f"Closes {closed_issues}")
                
            if body_parts:
                commit_msg += "\n\n" + "\n\n".join(body_parts)
                
            msg = commit_msg
            
            console.print(f"\n[bold yellow]Constructed Commit Message:[/bold yellow]")
            console.print(f"[dim]----------------------------------------[/dim]")
            console.print(f"[cyan]{msg}[/cyan]")
            console.print(f"[dim]----------------------------------------[/dim]")
            
            if not Confirm.ask("Proceed with this commit?", default=True):
                console.print("[yellow]Commit aborted by user.[/yellow]")
                raise typer.Exit(0)

        repo.git.add(A=True)
        repo.index.commit(msg)
        console.print(f"[bold green]✔ Saved snapshot:[/bold green] {msg}")
    except Exception as e:
        console.print(f"[bold red]Version control failed. Is this a Git repo? {e}[/bold red]")

def history(limit: int = typer.Option(10, "--limit", "-l", help="Number of commits to show")):
    """
    View a beautiful timeline of script modifications with usage details.
    
    This provides an easy-to-read log of all your previous `bfxpm save` snapshots. 
    It displays the Git commit hash, the author, the exact date, and the descriptive 
    message you saved for that milestone, allowing you to track project progress.
    """
    d = get_project_dir()
    try:
        repo = Repo(d)
        commits = list(repo.iter_commits())
        
        table = Table(title="Project Modification History")
        table.add_column("Hash", style="dim cyan")
        table.add_column("Author", style="magenta")
        table.add_column("Date", justify="left", style="green")
        table.add_column("Message", style="yellow")
        
        for c in commits[:limit]:
            table.add_row(
                c.hexsha[:7], 
                str(c.author),
                c.committed_datetime.strftime("%Y-%m-%d %H:%M"), 
                c.summary
            )
        console.print(table)
    except Exception as e:
         console.print(f"[bold red]History unavailable: {e}[/bold red]")

def sync(
    data: bool = typer.Option(False, "--data", help="Also sync the 'data/' folder using rsync"),
    remote_path: str = typer.Option(None, "--remote", help="Remote SSH path for data sync (e.g. user@hpc:/path/to/project)")
):
    """
    Sync your project progress (Git) and optionally your large data folder (Rsync).
    
    By default, this wraps `git push` to backup your code and configs. 
    Use the `--data` option to also sync the large files in your `data/` directory 
    (which are usually ignored by Git) to a remote SSH endpoint or cluster using `rsync`.
    """
    d = get_project_dir()
    
    # 1. Git Sync
    try:
        repo = Repo(d)
        
        # Proactively check for .env and other secrets
        sensitive_patterns = [
            r"\.env$",
            r"\.secrets?$",
            r".*key.*",
            r"id_rsa.*"
        ]
        
        untracked_sensitive = []
        tracked_sensitive = []
        
        for item in d.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(d)
                
                # Skip standard hidden directories (except actual .env/.secrets files)
                if any(part.startswith('.') and part not in ['.env', '.secrets'] for part in rel_path.parts):
                    continue
                if '.venv' in rel_path.parts or 'node_modules' in rel_path.parts:
                    continue
                    
                is_sensitive = False
                for pat in sensitive_patterns:
                    if re.match(pat, item.name, re.IGNORECASE):
                        is_sensitive = True
                        break
                        
                if is_sensitive:
                    rel_str = str(rel_path)
                    if rel_str in repo.untracked_files:
                        untracked_sensitive.append(rel_str)
                    else:
                        tracked_sensitive.append(rel_str)
                        
        if tracked_sensitive:
            console.print("\n[bold red]⚠️  CRITICAL WARNING: Tracked/Staged Sensitive Files Detected![/bold red]")
            for f in tracked_sensitive:
                console.print(f"  - [red]{f}[/red] (This file is tracked by Git and WILL be pushed!)")
            console.print("[yellow]It is highly recommended to unstage/untrack these files and add them to your .gitignore before syncing.[/yellow]")
            if not Confirm.ask("Do you still want to proceed with Git sync?", default=False):
                console.print("[yellow]Sync aborted by user.[/yellow]")
                raise typer.Exit(1)
                
        if untracked_sensitive:
            console.print("\n[bold yellow]⚠️  WARNING: Untracked Sensitive Files Detected in Workspace![/bold yellow]")
            for f in untracked_sensitive:
                console.print(f"  - [yellow]{f}[/yellow] (Not tracked yet, but present in workspace)")
            console.print("[yellow]Please ensure these files are added to your .gitignore to prevent accidental commits.[/yellow]\n")

        console.print("[yellow]Syncing Git repository...[/yellow]")
        origin = repo.remotes.origin
        origin.push()
        console.print("[bold green]✔ Git sync successful.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Git sync failed. Check remote network/origin setup: {e}[/bold red]")

    # 2. Data Sync (Rsync)
    if data:
        if not remote_path:
            console.print("[bold red]Error:[/bold red] --remote path is required for data sync.")
            raise typer.Exit(1)
            
        import subprocess
        data_path = d / "data"
        if not data_path.exists():
            console.print("[yellow]No 'data/' folder to sync.[/yellow]")
            return
            
        console.print(f"[yellow]Syncing data to {remote_path} via Rsync...[/yellow]")
        try:
            # -a: archive mode, -v: verbose, -z: compress, -P: partial/progress
            subprocess.run(["rsync", "-avzP", str(data_path) + "/", remote_path + "/data/"], check=True)
            console.print("[bold green]✔ Data sync successful.[/bold green]")
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Data sync failed: {e}[/bold red]")

def bump(
    dry_run: bool = typer.Option(
        False, 
        "--dry-run", 
        help="Calculate the version bump and show the changes without writing them."
    )
):
    """
    Automatically bump version, update changelog, and tag the release based on commit history.
    
    This command calculates the semantic version bump (Major/Minor/Patch) based on the Conventional 
    Commits since the last release tag, updates all package configuration version fields 
    (pyproject.toml, conda/meta.yaml, and __init__.py), appends new sections to CHANGELOG.md, 
    and automatically tags a new Git release.
    """
    d = get_project_dir()
    try:
        repo = Repo(d)
        
        # 1. Get all semver tags
        semver_regex = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
        valid_tags = []
        for t in repo.tags:
            match = semver_regex.match(t.name)
            if match:
                valid_tags.append((t, [int(x) for x in match.groups()]))
        
        # Sort tags by semver version parts
        valid_tags.sort(key=lambda x: x[1])
        
        last_tag_obj = valid_tags[-1][0] if valid_tags else None
        
        # 2. Collect commits since last tag
        if last_tag_obj:
            commits = list(repo.iter_commits(f"{last_tag_obj.commit.hexsha}..HEAD"))
            tag_name = last_tag_obj.name
        else:
            commits = list(repo.iter_commits())
            tag_name = "initial commit"
            
        if not commits:
            console.print("[yellow]No new commits found since last tag. Nothing to bump.[/yellow]")
            return
            
        console.print(f"[cyan]Found {len(commits)} commit(s) since {tag_name}[/cyan]")
        
        # 3. Analyze commits for bump level
        has_feat = False
        has_breaking = False
        parsed_commits = []
        
        for c in commits:
            msg = c.message.strip()
            summary = c.summary.strip()
            is_breaking = "BREAKING CHANGE:" in msg
            
            # Conventional commit: type(scope)!: subject
            match = re.match(r"^(\w+)(?:\(([^)]+)\))?(!)?:\s*(.*)$", summary)
            c_type = "chore"
            c_scope = ""
            c_subject = summary
            
            if match:
                c_type, c_scope, c_excl, c_subject = match.groups()
                if c_excl or is_breaking:
                    has_breaking = True
                if c_type == "feat":
                    has_feat = True
            
            parsed_commits.append({
                "hash": c.hexsha[:7],
                "type": c_type,
                "scope": c_scope or "",
                "subject": c_subject,
                "is_breaking": is_breaking or bool(match and match.group(3)),
                "author": str(c.author),
                "date": c.committed_datetime.strftime("%Y-%m-%d")
            })
            
        if has_breaking:
            bump_type = "major"
        elif has_feat:
            bump_type = "minor"
        else:
            bump_type = "patch"
            
        # 4. Calculate new version
        current_ver = get_current_version(d)
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", current_ver)
        if not match:
            console.print(f"[bold red]Could not parse current version '{current_ver}' as semver.[/bold red]")
            raise typer.Exit(1)
            
        major, minor, patch = map(int, match.groups())
        if bump_type == "major":
            new_version = f"{major + 1}.0.0"
        elif bump_type == "minor":
            new_version = f"{major}.{minor + 1}.0"
        else:
            new_version = f"{major}.{minor}.{patch + 1}"
            
        console.print(f"Calculated Version Bump: [bold green]{current_ver} -> {new_version}[/bold green] ([magenta]{bump_type}[/magenta])")
        
        # 5. Format Changelog Entry
        today = datetime.date.today().strftime("%Y-%m-%d")
        added = []
        fixed = []
        changed = []
        breaking = []
        
        for pc in parsed_commits:
            scope_pfx = f"**{pc['scope']}**: " if pc['scope'] else ""
            item = f"- {scope_pfx}{pc['subject']} ({pc['hash']})"
            if pc['is_breaking']:
                breaking.append(item)
            elif pc['type'] == "feat":
                added.append(item)
            elif pc['type'] == "fix":
                fixed.append(item)
            else:
                changed.append(item)
                
        changelog_entry = f"## [{new_version}] - {today}\n\n"
        if breaking:
            changelog_entry += "### Breaking Changes\n" + "\n".join(breaking) + "\n\n"
        if added:
            changelog_entry += "### Added\n" + "\n".join(added) + "\n\n"
        if fixed:
            changelog_entry += "### Fixed\n" + "\n".join(fixed) + "\n\n"
        if changed:
            changelog_entry += "### Changed / Other\n" + "\n".join(changed) + "\n\n"
            
        # 6. Apply edits (unless dry-run)
        if dry_run:
            console.print("\n[yellow]--- DRY RUN: Review Proposed Changes ---[/yellow]")
            console.print(f"[bold]New Changelog Section:[/bold]\n{changelog_entry}")
            return
            
        # Update pyproject.toml
        pyproject_path = d / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "r") as f:
                content = f.read()
            new_content = re.sub(r'^(version\s*=\s*["\'])([^"\']*)(["\'])', rf'\g<1>{new_version}\g<3>', content, flags=re.MULTILINE)
            with open(pyproject_path, "w") as f:
                f.write(new_content)
                
        # Update conda/meta.yaml
        conda_path = d / "conda" / "meta.yaml"
        if conda_path.exists():
            with open(conda_path, "r") as f:
                content = f.read()
            new_content = re.sub(r'(set version\s*=\s*["\'])([^"\']*)(["\'])', rf'\g<1>{new_version}\g<3>', content)
            with open(conda_path, "w") as f:
                f.write(new_content)
                
        # Update src/bfxpm/__init__.py
        init_path = d / "src" / "bfxpm" / "__init__.py"
        if init_path.exists():
            with open(init_path, "r") as f:
                content = f.read()
            new_content = re.sub(r'^(__version__\s*=\s*["\'])([^"\']*)(["\'])', rf'\g<1>{new_version}\g<3>', content, flags=re.MULTILINE)
            with open(init_path, "w") as f:
                f.write(new_content)
                
        # Update CHANGELOG.md
        changelog_path = d / "CHANGELOG.md"
        if changelog_path.exists():
            with open(changelog_path, "r") as f:
                cl_content = f.read()
            idx = cl_content.find("## [")
            if idx != -1:
                new_cl_content = cl_content[:idx] + changelog_entry + cl_content[idx:]
            else:
                new_cl_content = cl_content + "\n" + changelog_entry
            with open(changelog_path, "w") as f:
                f.write(new_cl_content)
                
        # Commit & tag
        repo.git.add("pyproject.toml", "conda/meta.yaml", "src/bfxpm/__init__.py", "CHANGELOG.md")
        commit_msg = f"chore: release v{new_version}"
        repo.index.commit(commit_msg)
        
        repo.create_tag(f"v{new_version}", message=f"Release version {new_version}")
        console.print(f"[bold green]✔ Successfully bumped to v{new_version} and tagged the release![/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]Bumping failed: {e}[/bold red]")

