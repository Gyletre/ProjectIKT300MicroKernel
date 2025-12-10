from .mqtt_client import MQTTClient

class AbstractPlugin(MQTTClient):
    """Subscribe to topics with self._Subscribe(topic). \n
    Then override self._OnDataRecieved() and use self._SendData() to add plugin specific implementation"""
    def __init__(self, config=None):
        super().__init__(config)

    def ShutDown(self):
        del(self)

    