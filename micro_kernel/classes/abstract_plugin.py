from abc import ABC, abstractmethod
from classes.i_message_client import IMessageClient
from time import time
from asyncio import run

class AbstractPlugin():
    def __init__(self,id,brokerIP,port):
        self.id = id
        self.brokerIP = brokerIP
        self.client = IMessageClient()
        # connect to broker
        run(self.HeartBeat)
        super().__init__()

    def ShutDown(self):
        del(self)

    