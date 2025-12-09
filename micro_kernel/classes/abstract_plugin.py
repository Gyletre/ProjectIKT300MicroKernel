from abc import ABC, abstractmethod
from classes.i_message_client import IMessageClient
from time import time
from asyncio import run
from classes.mqtt_client import MQTTClient

class AbstractPlugin(MQTTClient):
    """Subscribe to topics with self._Subscribe(topic). \n
    Then override self._OnDataRecieved() and self.SendData() to add plugin specific implementation"""
    def __init__(self, config, on_message):
        super().__init__(config, on_message)

    def ShutDown(self):
        del(self)

    