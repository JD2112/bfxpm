import typer
import time
import json
from pathlib import Path
from bfxpm.utils import console, get_project_dir

flow_app = typer.Typer(help="Record your terminal session into reproducible scripts.")

@flow_app.command("start")
def start():
    """Start recording a terminal session."""
    d = get_project_dir()
    record_file = d / ".bfxpm" / "recording.json"
    record_file.parent.mkdir(parents=True, exist_ok=True)
    
    if record_file.exists():
        console.print("[yellow]Recording is already in progress.[/yellow]")
        return
        
    start_time = time.time()
    with open(record_file, "w") as f:
        json.dump({"start_time": start_time}, f)
        
    console.print("[bold green]● Recording started.[/bold green]")
    console.print("[dim]Every command you run from now on will be captured when you run 'bfxpm flow stop'.[/dim]")

@flow_app.command("stop")
def stop(name: str = typer.Argument("analysis_script", help="Name of the generated script")):
    """Stop recording and save the commands to a script."""
    d = get_project_dir()
    record_file = d / ".bfxpm" / "recording.json"
    
    if not record_file.exists():
        console.print("[red]No recording is in progress. Run 'bfxpm flow start' first.[/red]")
        return
        
    with open(record_file, "r") as f:
        data = json.load(f)
        start_time = data["start_time"]
    
    record_file.unlink()
    
    console.print("[yellow]Extracting flow from shell history...[/yellow]")
    
    # Check history files
    history_files = [Path.home() / ".zsh_history", Path.home() / ".bash_history"]
    commands = []
    
    for hf in history_files:
        if hf.exists():
            # For simplicity, we grab the last 50-100 commands if they were after start_time.
            # Real timestamp parsing depends on shell config (e.g. EXTENDED_HISTORY in zsh).
            # We'll do a simple recent-capture if parsing fails.
            with open(hf, "rb") as f:
                lines = f.readlines()
                for line in lines[-50:]:
                    try:
                        decoded = line.decode('utf-8', errors='ignore').strip()
                        if not decoded: continue
                        # ZSH extended history looks like ': 1712781212:0;ls'
                        if decoded.startswith(": "):
                            parts = decoded.split(";", 1)
                            if len(parts) == 2:
                                t_str = parts[0].split(":")[1].strip()
                                if int(t_str) >= int(start_time):
                                    cmd = parts[1].strip()
                                    if "bfxpm flow" not in cmd and cmd not in commands:
                                        commands.append(cmd)
                        else:
                            # Just add it if we can't parse time (fall back)
                            if "bfxpm" not in decoded and decoded not in commands:
                                commands.append(decoded)
                    except:
                        continue

    if not commands:
        console.print("[yellow]No new commands found in history.[/yellow]")
        return

    out_file = d / "scripts" / f"{name}_{int(time.time())}.sh"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out_file, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"# BfxPM Recorded Flow: {time.ctime()}\n\n")
        for cmd in commands:
            f.write(f"{cmd}\n")
            
    console.print(f"[bold green]✔ Recording stopped. Script saved to {out_file.relative_to(d)}[/bold green]")
