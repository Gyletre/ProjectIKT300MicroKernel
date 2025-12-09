import paho.mqtt.client as mqtt
from classes.i_message_client import IMessageClient
from dataclasses import dataclass
import sys


@dataclass
class MQTTClientConfig:
    pid: int
    broker: str
    port: int

    def from_sys(self):
        return MQTTClientConfig(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))


class MQTTClient(IMessageClient):
    KEEPALIVE = 60

    def __init__(self, config: MQTTClientConfig) -> None:
        self.broker = config.broker
        self.port = config.port
        self.id = config.pid

        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.on_message = self._OnDataRecieved

        self.connected = False
        self._ConnectToBroker()

        self.client.loop_start()

    def _ConnectToBroker(self):
        self.client.connect(self.broker, self.port, self.KEEPALIVE)

    def _OnDataRecieved(self, client, userdata, message):
        pass
    
    def _SendData(self, topic, payload, qos=0, retain=False):
        if not self.connected:
            raise RuntimeError('Not connected to broker.')
        
        self.client.publish(topic, payload, qos, retain)

    def _Subscribe(self, topic, qos=0):
        if not self.connected:
            raise RuntimeError('Not connected to broker.')
        
        self.client.subscribe(topic, qos)

    def __on_connect(self, client, userdata, flags, rc):
        if rc == 0: self.connected = True

    def __on_disconnect(self, client, userdata, rc):
        self.connected = False
    

