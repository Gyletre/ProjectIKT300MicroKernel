from typing import List
from pydantic import BaseModel


from ..models.MQTTConfig import MQTTConfig
from ..models.PluginConfig import PluginConfig


class AppConfig(BaseModel):
    mqtt: MQTTConfig
    plugins: List[PluginConfig] = []
    plugins_directory: str = "./plugins"
