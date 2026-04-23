import os
from typing import Optional, List, Dict, Any
from bfxpm.ai_config import AIConfig
from bfxpm.utils import console

class AIClient:
    def __init__(self, config: AIConfig):
        self.config = config
        self._genai_client = None

    def get_genai_client(self):
        """Returns the initialized Google GenAI Client (Lazy Import)."""
        if self._genai_client:
            return self._genai_client

        if self.config.provider == "gemini":
            api_key = self.config.get_api_key("gemini")
            if not api_key:
                raise ValueError("Gemini API key not configured. Run 'bfxpm ai setup'.")
            
            from google import genai
            self._genai_client = genai.Client(api_key=api_key)
            return self._genai_client
        
        return None

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Sends a conversation to the configured provider and returns the response string."""
        provider = self.config.provider
        model_name = self.config.model

        if provider == "ollama":
            import ollama
            response = ollama.chat(model=model_name, messages=messages)
            return response['message']['content']
        
        elif provider == "gemini":
            client = self.get_genai_client()
            response = client.models.generate_content(
                model=model_name,
                contents=[m['content'] for m in messages]
            )
            return response.text
        
        else:
            # Use LiteLLM for OpenAI, Anthropic, etc.
            import os
            import litellm
            api_key = self.config.get_api_key()
            if api_key:
                env_map = {
                    "openai": "OPENAI_API_KEY",
                    "anthropic": "ANTHROPIC_API_KEY",
                    "groq": "GROQ_API_KEY",
                    "mistral": "MISTRAL_API_KEY"
                }
                env_var = env_map.get(provider)
                if env_var:
                    os.environ[env_var] = api_key
            
            prefix_map = {
                "openai": "openai/",
                "anthropic": "anthropic/",
                "groq": "groq/",
                "mistral": "mistral/"
            }
            prefix = prefix_map.get(provider, "")
            response = litellm.completion(model=f"{prefix}{model_name}", messages=messages)
            return response.choices[0].message.content

    def test_connection(self) -> bool:
        """Verifies connection to the local or cloud service."""
        try:
            if self.config.provider == "ollama":
                import ollama
                ollama.list()
                return True
            elif self.config.provider == "gemini":
                client = self.get_genai_client()
                return client is not None
            else:
                # Basic key check for others
                return self.config.get_api_key() is not None
        except Exception as e:
            console.print(f"[red]Connection Test Failed:[/red] {e}")
            return False
