import json
from pathlib import Path
from micro_kernel.models.AppConfig import AppConfig


class ConfigService:
    def __init__(self, app_config: AppConfig):
        self.app_config: AppConfig = app_config
    
    @staticmethod
    def load_from_json(config_path: str) -> 'ConfigService':
        """Load and validate AppConfig from a JSON file."""
        path = Path(config_path)

        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Validate and create AppConfig instance
        app_config = AppConfig(**data)

        return ConfigService(app_config)