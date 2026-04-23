from dataclasses import dataclass
from typing import List, Dict, Optional
from bfxpm.ai_client import AIClient
from bfxpm.ai_config import AIConfig
from bfxpm.utils import console
from bfxpm.safety import SafetyLayer

# Base classes from smolagents are relatively light, 
# but we import them here to allow class inheritance.
# The heavy SDKs (google-genai, litellm) will be imported inside methods.
import smolagents

@dataclass
class ModelOutput:
    content: str

class GoogleGenAIModel(smolagents.Model):
    """Custom smolagents wrapper for the new google-genai SDK."""
    def __init__(self, model_id: str, api_key: str, **kwargs):
        super().__init__(model_id=model_id, **kwargs)
        from google import genai
        self.client = genai.Client(api_key=api_key)

    def generate(self, messages: List[Dict[str, str]], stop_sequences: List[str] = None, **kwargs) -> ModelOutput:
        contents = []
        for m in messages:
            role = "user" if m["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": m["content"]}]})
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=contents,
            config={"stop_sequences": stop_sequences} if stop_sequences else None
        )
        return ModelOutput(content=response.text)

class BioAssistant:
    def __init__(self, config: AIConfig, client: AIClient):
        self.config = config
        self.client = client
        self.safety = SafetyLayer(config)
        
        # Initialize the appropriate smolagents model
        if config.provider == "gemini":
            self.model = GoogleGenAIModel(model_id=config.model, api_key=config.get_api_key("gemini"))
        else:
            import os
            from smolagents import LiteLLMModel
            
            api_key = config.get_api_key()
            if api_key:
                # Set env var for LiteLLM
                env_map = {
                    "openai": "OPENAI_API_KEY",
                    "anthropic": "ANTHROPIC_API_KEY",
                    "groq": "GROQ_API_KEY",
                    "mistral": "MISTRAL_API_KEY"
                }
                env_var = env_map.get(config.provider)
                if env_var:
                    os.environ[env_var] = api_key

            # Map provider to LiteLLM prefix
            prefix_map = {
                "ollama": "ollama_chat/",
                "openai": "openai/",
                "anthropic": "anthropic/",
                "groq": "groq/",
                "mistral": "mistral/"
            }
            prefix = prefix_map.get(config.provider, "")
            self.model = LiteLLMModel(model_id=f"{prefix}{config.model}")
        
    def run(self, prompt: str):
        """Runs the agent with the given prompt."""
        from smolagents import CodeAgent
        from bfxpm.agents.tools import BIO_TOOLS
        
        agent = CodeAgent(
            tools=BIO_TOOLS,
            model=self.model,
            add_base_tools=True
        )
        
        contextual_prompt = (
            f"Context: You are the BfxPM AI Assistant. Current Project: {self.config.project_dir}\n"
            f"User Query: {prompt}"
        )
        
        try:
            return agent.run(contextual_prompt)
        except Exception as e:
            return f"Agent Error: {str(e)}"
