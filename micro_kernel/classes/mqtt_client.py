import paho.mqtt.client as mqtt
from micro_kernel.i_message_client import IMessageClient
from dataclasses import dataclass
import sys
import json


MQTTMessage = mqtt.MQTTMessage


@dataclass
class MQTTClientConfig:
    pid: int
    broker: str
    port: int

    @staticmethod
    def from_sys():
        return MQTTClientConfig(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))


class MQTTClient(IMessageClient):
    KEEPALIVE = 10

    def __init__(self, config: MQTTClientConfig|None = None) -> None:
        if config is None:
            config = MQTTClientConfig.from_sys()

        self.broker = config.broker
        self.port = config.port
        self.id = config.pid

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # type: ignore
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.on_message = self._OnDataRecieved

        self.connected = False
        self._ConnectToBroker()

        self.client.will_set('plugins/morgue', json.dumps({'type': 'Error', 'payload': {'id': self.id}}))

        self.client.loop_start()

    def _ConnectToBroker(self):
        self.client.connect(self.broker, self.port, self.KEEPALIVE)

    def _OnDataRecieved(self, client, userdata, message: mqtt.MQTTMessage):
        pass
    
    def _SendData(self, topic, payload, qos=0, retain=False):
        if not self.connected:
            raise RuntimeError('Not connected to broker.')
        
        self.client.publish(topic, payload, qos, retain)

    def _Subscribe(self, topic, qos=0):
        if not self.connected:
            raise RuntimeError('Not connected to broker.')
        
        self.client.subscribe(topic, qos)

    def __on_connect(self, client, userdata, flags, rc, *_):
        if rc == 0:
            self.connected = True
            print('connected to broker')

    def __on_disconnect(self, client, userdata, rc, *_):
        self.connected = False
        print('disconnected from broker')


if __name__ == '__main__':
    MQTTClient(MQTTClientConfig(1, 'localhost', 9001))
    