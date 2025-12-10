from pydantic import BaseModel


class PluginConfig(BaseModel):
    name: str
    path: str
    enabled: bool = True
    restart_on_failure: bool = True