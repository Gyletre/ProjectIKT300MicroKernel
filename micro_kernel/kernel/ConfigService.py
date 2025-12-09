import json
from pathlib import Path
from typing import Optional
from micro_kernel.models.AppConfig import AppConfig


class ConfigService:
    def __init__(self):
        self.app_config: Optional[AppConfig] = None
        
    def load_configs_from_json(self, path: str) -> AppConfig:
        """Load and validate AppConfig from a JSON file."""
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Validate and create AppConfig instance
        self.app_config = AppConfig(**data)

        return self.app_config