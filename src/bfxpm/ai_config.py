import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from bfxpm.utils import get_project_dir

CONFIG_FILENAME = "ai_config.yaml"

class AIConfig:
    def __init__(self):
        self.project_dir = get_project_dir()
        self.config_dir = self.project_dir / ".bfxpm"
        self.config_path = self.config_dir / CONFIG_FILENAME
        self._config: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            return self._get_defaults()
        
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f) or self._get_defaults()
        except Exception:
            return self._get_defaults()

    def _get_defaults(self) -> Dict[str, Any]:
        return {
            "provider": "ollama",
            "model": "gemma2:2b",
            "keys": {},  # Dictionary to store multiple API keys
            "local_url": "http://localhost:11434",
            "safety": {
                "require_confirmation": True,
                "auto_backup": True,
                "backup_dir": ".bfxpm/backups"
            }
        }

    def save(self):
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, "w") as f:
            yaml.dump(self._config, f, default_flow_style=False)

    @property
    def provider(self) -> str:
        return self._config.get("provider", "ollama")

    @provider.setter
    def provider(self, value: str):
        self._config["provider"] = value

    @property
    def model(self) -> str:
        return self._config.get("model", "gemma2:2b")

    @model.setter
    def model(self, value: str):
        self._config["model"] = value

    def get_api_key(self, provider: Optional[str] = None) -> Optional[str]:
        p = provider or self.provider
        return self._config.get("keys", {}).get(p)

    def set_api_key(self, provider: str, key: str):
        if "keys" not in self._config:
            self._config["keys"] = {}
        self._config["keys"][provider] = key

    @property
    def backup_dir(self) -> Path:
        rel_path = self._config.get("safety", {}).get("backup_dir", ".bfxpm/backups")
        return self.project_dir / rel_path

    def get_safety_settings(self) -> Dict[str, Any]:
        return self._config.get("safety", {})

    def set_safety_setting(self, key: str, value: Any):
        if "safety" not in self._config:
            self._config["safety"] = {}
        self._config["safety"][key] = value
