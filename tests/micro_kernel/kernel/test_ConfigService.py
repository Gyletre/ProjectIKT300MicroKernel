# tests/micro_kernel/kernel/test_ConfigService.py
import json
import pytest
from pathlib import Path
from pydantic import ValidationError

from micro_kernel.kernel.ConfigService import ConfigService
from micro_kernel.models.AppConfig import AppConfig
from micro_kernel.models.MQTTConfig import MQTTConfig
from micro_kernel.models.PluginConfig import PluginConfig


@pytest.fixture
def valid_config_data():
    return {
        "mqtt": {
            "broker_host": "localhost",
            "broker_port": 1883,
            "username": "user",
            "password": "pass",
            "use_tls": False
        },
        "plugins_directory": "./plugins",
        "plugins": [
            {"name": "MetricsLogger", "path": "./plugins/metrics_logger.py", "enabled": True}
        ]
    }


def test_load_configs_from_json_success(tmp_path, valid_config_data):
    """Should load and validate AppConfig from a valid JSON file."""
    config_path = tmp_path / "appsettings.json"
    config_path.write_text(json.dumps(valid_config_data), encoding="utf-8")

    service = ConfigService()
    config = service.load_configs_from_json(str(config_path))

    assert isinstance(config, AppConfig)
    assert isinstance(config.mqtt, MQTTConfig)
    assert config.mqtt.broker_host == "localhost"
    assert config.mqtt.broker_port == 1883
    assert len(config.plugins) == 1
    assert isinstance(config.plugins[0], PluginConfig)
    assert config.plugins[0].name == "MetricsLogger"
    assert service.app_config is config  # cached instance


def test_load_configs_from_json_missing_file():
    """Should raise FileNotFoundError and not set app_config."""
    service = ConfigService()
    assert service.app_config is None  # before load
    with pytest.raises(FileNotFoundError):
        service.load_configs_from_json("nonexistent.json")
    assert service.app_config is None  # should still be None


def test_load_configs_from_json_invalid_schema(tmp_path, valid_config_data):
    """Should raise ValidationError and not set app_config."""
    invalid_data = valid_config_data.copy()
    invalid_data["mqtt"].pop("broker_host")  # remove required field

    config_path = tmp_path / "invalid.json"
    config_path.write_text(json.dumps(invalid_data), encoding="utf-8")

    service = ConfigService()
    assert service.app_config is None  # before load
    with pytest.raises(ValidationError):
        service.load_configs_from_json(str(config_path))
    assert service.app_config is None  # should still be None
