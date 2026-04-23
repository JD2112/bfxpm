import typer
from bfxpm.utils import console, smart_prompt, smart_confirm
from bfxpm.ai_config import AIConfig

ai_app = typer.Typer(help="Agentic AI for bioinformatics project management")

@ai_app.command("setup")
def setup():
    import typer
    from rich.panel import Panel
    """Interactively setup AI service, models, and security."""
    config = AIConfig()
    
    console.print(Panel.fit("BfxPM AI Setup Assistant", style="bold green"))
    
    # 1. Provide Context on Privacy
    console.print("\n[bold]Privacy Notice:[/bold]")
    console.print("To ensure data stays in the [bold blue]EU[/bold blue], we recommend local execution using Ollama.")
    
    # 2. Choose Provider
    providers = ["ollama", "gemini", "openai", "anthropic", "groq", "mistral"]
    console.print("\n[bold]Select AI Provider:[/bold] (Type 'q' to quit)")
    for i, p in enumerate(providers):
        console.print(f"[{i+1}] {p}")
    
    choice = smart_prompt("Select choice", default="1")
    try:
        provider = providers[int(choice) - 1]
    except (ValueError, IndexError):
        provider = "ollama"
        
    # GDPR / Data Privacy Warning for Cloud Providers
    if provider != "ollama":
        console.print(Panel(
            "[bold red]Data Privacy Warning (GDPR)[/bold red]\n"
            f"You have selected [bold cyan]{provider}[/bold cyan] as your AI provider.\n"
            "This service processes data [bold red]outside the EU[/bold red]. Prompts, project metadata, "
            "and file structures may be transmitted to external servers.\n\n"
            "By proceeding, you acknowledge that your research data may leave the EU region.",
            title="⚠️ Privacy Alert",
            border_style="red"
        ))
        confirm = smart_confirm("Do you want to proceed with this cloud provider?", default=False)
        if not confirm:
            console.print("[yellow]Setup aborted by user to maintain data residency.[/yellow]")
            return

    config.provider = provider

    # Provider-specific settings
    defaults = {
        "ollama": ("gemma2:2b", None),
        "gemini": ("gemini-1.5-flash", "Gemini API Key"),
        "openai": ("gpt-4o", "OpenAI API Key"),
        "anthropic": ("claude-3-5-sonnet-20240620", "Anthropic API Key"),
        "groq": ("llama-3.3-70b-versatile", "Groq API Key"),
        "mistral": ("mistral-large-latest", "Mistral API Key")
    }
    
    default_model, key_label = defaults.get(provider, ("gemma2:2b", None))
    
    if key_label:
        existing_key = config.get_api_key(provider)
        key_prompt = f"Insert your {key_label}"
        if existing_key:
            key_prompt += " (leave blank to keep current)"
        
        api_key = smart_prompt(key_prompt, password=True, default="" if existing_key else None)
        if api_key and api_key != "":
            config.set_api_key(provider, api_key)
    
    model = smart_prompt(f"Select model for {provider}", default=default_model)
    config.model = model

    # 3. Safety Settings
    auto_backup = smart_confirm("Enable automatic backups before destructive actions?", default=True)
    config.set_safety_setting("auto_backup", auto_backup)
    
    config.save()
    console.print("[bold green]Success![/bold green] Configuration saved to .bfxpm/ai_config.yaml")

@ai_app.command("ask")
def ask(prompt: str = typer.Argument(..., help="The question or task for the AI")):
    import typer
    from rich.panel import Panel
    from rich.markdown import Markdown
    from bfxpm.ai_client import AIClient
    from bfxpm.agents.bio_agent import BioAssistant
    
    config = AIConfig()
    client = AIClient(config)
    
    if not client.test_connection():
        console.print("[red]Error:[/red] Could not connect to AI service. Run 'bfxpm ai setup' first.")
        return

    assistant = BioAssistant(config, client)
    
    # smolagents does its own printing, so we just call run
    response = assistant.run(prompt)
    
    console.print(Panel(Markdown(str(response)), title="Final Answer", border_style="blue"))

@ai_app.command("chat")
def chat():
    import typer
    from rich.panel import Panel
    from rich.markdown import Markdown
    from bfxpm.ai_client import AIClient
    from bfxpm.agents.bio_agent import BioAssistant
    
    config = AIConfig()
    client = AIClient(config)
    
    if not client.test_connection():
        console.print("[red]Error:[/red] Could not connect to AI service. Run 'bfxpm ai setup' first.")
        return

    assistant = BioAssistant(config, client)
    
    console.print(Panel("Welcome to [bold cyan]BfxPMAI Chat[/bold cyan]\nType 'exit' to quit.", border_style="green"))
    
    while True:
        user_input = typer.prompt("You")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        response = assistant.run(user_input)
        # Note: smolagents CodeAgent prints the thought panels internally
        console.print(Panel(Markdown(str(response)), title="BioAssistant Final Answer", border_style="blue"))
