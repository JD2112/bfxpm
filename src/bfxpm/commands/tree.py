import typer
import os
from pathlib import Path
from rich.tree import Tree
from bfxpm.utils import console

def tree_cmd(
    path: str = typer.Argument(".", help="Directory to show tree for"),
    pager: bool = typer.Option(True, "--pager/--no-pager", help="Use a pager for the output"),
    show_hidden: bool = typer.Option(False, "--all", "-a", help="Show hidden files and directories"),
    icons: bool = typer.Option(False, "--icons", help="Show emojis/icons")
):
    """Show a beautiful tree view of the directory and files."""
    target_path = Path(path).resolve()
    if not target_path.exists():
        console.print(f"Path [bold red]{path}[/bold red] does not exist.")
        return

    root_label = f"[bold cyan]{target_path.name}/[/bold cyan]"
    if icons:
        root_label = f":open_file_folder: {root_label}"
        
    tree_obj = Tree(
        root_label,
        guide_style="bold bright_black",
    )

    def add_to_tree(directory: Path, tree: Tree):
        try:
            items = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            return
            
        for p in items:
            # Skip hidden files unless show_hidden is True
            if not show_hidden:
                if p.name.startswith('.') or p.name == '__pycache__' or p.name == 'node_modules':
                    continue
            else:
                # Even with --all, we might want to skip some specific massive internals if needed, 
                # but usually --all means everything.
                if p.name == '__pycache__' or p.name == 'node_modules':
                    continue

            if p.is_dir():
                label = f"[bold cyan]{p.name}/[/bold cyan]"
                if icons:
                    label = f":open_file_folder: {label}"
                branch = tree.add(label)
                add_to_tree(p, branch)
            else:
                label = f"[white]{p.name}[/white]"
                if icons:
                    label = f":page_facing_up: {label}"
                tree.add(label)

    add_to_tree(target_path, tree_obj)
    
    if pager:
        # On Unix systems, 'less -R' is needed to show ANSI colors
        old_less = os.environ.get("LESS", "")
        os.environ["LESS"] = "-R"
        try:
            with console.pager(styles=True):
                console.print(tree_obj)
        finally:
            os.environ["LESS"] = old_less
    else:
        console.print(tree_obj)
