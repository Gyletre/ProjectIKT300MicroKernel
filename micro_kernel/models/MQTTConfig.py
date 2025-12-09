from typing import Optional
from pydantic import BaseModel, Field

class MQTTConfig(BaseModel):
    broker_host: str = Field(..., description="MQTT broker hostname")
    broker_port: int = Field(..., ge=1, le=65535)