import typer
import inspect
from bfxpm import __version__
from bfxpm.commands.init_cmd import init_app
from bfxpm.commands.scan import scan
from bfxpm.commands.organize import organize
from bfxpm.commands.clean import clean_app
from bfxpm.commands.env_cmd import env_app
from bfxpm.commands.pipeline_cmd import pipeline_app
from bfxpm.commands.fetch_cmd import fetch_app
from bfxpm.commands.git_cmds import save, history, sync, bump
from bfxpm.commands.tree import tree_cmd
from bfxpm.commands.misc import (
    compress,
    login,
    logout,
    run_history,
    show,
    report,
    update,
    list_projects,
)
from bfxpm.commands.modify import modify
from bfxpm.commands.map_cmd import create_map
from bfxpm.commands.integrity import checksum_app
from bfxpm.commands.flow import flow_app
from bfxpm.commands.deposit import deposit_app
from bfxpm.commands.ai_cmd import ai_app


from bfxpm.utils import console

help_text = f"[bold green]Developer:[/bold green] Jyotirmoy Das\n\n" \
            f"[bold green]Maintainer:[/bold green] Jyotirmoy Das\n\n" \
            f"[bold green]Version:[/bold green] {__version__}\n\n" \
            f"Bioinformatician's Project Manager CLI"

app = typer.Typer(help=help_text, rich_markup_mode="rich")

@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """
    Bioinformatician's Project Manager CLI
    """
    if ctx.invoked_subcommand is None:
        header = r"""[bold cyan]
▄ ▐▘  ▄▖▖  ▖   ▄ ▘  ▘  ▐▘         ▗ ▘  ▘    ▌    ▄▖     ▘    ▗   ▖  ▖            
▙▘▜▘▚▘▙▌▛▖▞▌▖  ▙▘▌▛▌▌▛▌▜▘▛▌▛▘▛▛▌▀▌▜▘▌▛▘▌▀▌▛▌ ▛▘  ▙▌▛▘▛▌ ▌█▌▛▘▜▘  ▛▖▞▌▀▌▛▌▀▌▛▌█▌▛▘
▙▘▐ ▞▖▌ ▌▝ ▌▖  ▙▘▌▙▌▌▌▌▐ ▙▌▌ ▌▌▌█▌▐▖▌▙▖▌█▌▌▌ ▄▌  ▌ ▌ ▙▌ ▌▙▖▙▖▐▖  ▌▝ ▌█▌▌▌█▌▙▌▙▖▌ 
                                                       ▙▌                  ▄▌    
[/bold cyan]"""
        console.print(header, soft_wrap=True)
        # If no subcommand, always show help
        console.print(ctx.get_help())
        raise typer.Exit()

app.command(name="init")(init_app)
app.command(name="scan")(scan)
app.command(name="organize")(organize)
app.command(name="tree")(tree_cmd)
app.command(name="projects")(list_projects)
app.command(name="compress")(compress)
app.command(name="save")(save)
app.command(name="bump")(bump)
app.command(name="history")(history)
app.command(name="sync")(sync)
app.command(name="login")(login)
app.command(name="logout")(logout)
app.command(name="run_history")(run_history)
app.command(name="show")(show)
app.command(name="report")(report)
app.command(name="update")(update)
app.command(name="modify")(modify)
app.command(name="map")(create_map)

app.add_typer(clean_app, name="clean", help="Manage and clean project disk space")
app.add_typer(env_app, name="env", help="Manage standard bioinformatics environments")
app.add_typer(pipeline_app, name="pipeline", help="Scaffold analysis pipelines")
app.add_typer(fetch_app, name="fetch", help="Fetch and route external biological data")
app.add_typer(checksum_app, name="checksum", help="Manage data integrity using checksums")
app.add_typer(flow_app, name="flow", help="Record terminal sessions into scripts")
app.add_typer(deposit_app, name="deposit", help="Deposit project data to public repositories")
app.add_typer(ai_app, name="ai", help="Agentic AI for bioinformatics project management")


def main():
    app()


if __name__ == "__main__":
    main()
