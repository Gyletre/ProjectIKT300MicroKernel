import paho.mqtt.client as mqtt
from dataclasses import dataclass
import sys


@dataclass
class MQTTClientConfig:
    pid: int
    broker: str
    port: int

    @staticmethod
    def from_sys():
        return MQTTClientConfig(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))


class MQTTClient:
    KEEPALIVE = 60

    def __init__(self, config: MQTTClientConfig|None, on_message) -> None:
        if config is None:
            config = MQTTClientConfig.from_sys()

        self.broker = config.broker
        self.port = config.port
        self.id = config.pid

        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = on_message

        self.connected = False
        self.connect()

        self.client.loop_start()

    def connect(self):
        self.client.connect(self.broker, self.port, self.KEEPALIVE)
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0: self.connected = True

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False

    def publish(self, topic, payload, qos=0, retain=False):
        if not self.connected:
            raise RuntimeError('Not connected to broker.')
        
        self.client.publish(topic, payload, qos, retain)
    
    def subscribe(self, topic, qos=0):
        if not self.connected:
            raise RuntimeError('Not connected to broker.')
        
        self.client.subscribe(topic, qos)
