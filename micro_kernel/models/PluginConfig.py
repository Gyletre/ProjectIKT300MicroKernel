from typing import Optional
from pydantic import BaseModel

from micro_kernel.models.MQTTConfig import MQTTConfig

class PluginConfig(BaseModel):
    name: str
    path: str
    enabled: bool = True
    restart_on_failure: bool = True