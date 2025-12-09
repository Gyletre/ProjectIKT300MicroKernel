from typing import List
from pydantic import BaseModel, Field

from micro_kernel.models.MQTTConfig import MQTTConfig
from micro_kernel.models.PluginConfig import PluginConfig

class AppConfig(BaseModel):
    mqtt: MQTTConfig
    plugins: List[PluginConfig] = []
    plugins_directory: str = "./plugins"
