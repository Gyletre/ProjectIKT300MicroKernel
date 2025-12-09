import paho.mqtt.client as mqtt
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class IEventBusConfig:
    broker: str
    port: int


class IEventBus(ABC):
    KEEPALIVE = 60

    def __init__(self, event_bus_config: IEventBusConfig) -> None:
        self.broker = event_bus_config.broker
        self.port = event_bus_config.port

        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self.on_message

        self.connected = False
        self.connect()

        self.client.loop_start()

    def connect(self):
        self.client.connect(self.broker, self.port, self.KEEPALIVE)
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0: self.connected = True

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False

    @abstractmethod
    def on_message(self, client, userdata, msg: mqtt.MQTTMessage):
        pass

    def publish(self, topic, payload, qos=0, retain=False):
        if not self.connected:
            raise RuntimeError('Not connected to broker.')
        
        self.client.publish(topic, payload, qos, retain)
    
    def subscribe(self, topic, qos=0):
        if not self.connected:
            raise RuntimeError('Not connected to broker.')
        
        self.client.subscribe(topic, qos)
