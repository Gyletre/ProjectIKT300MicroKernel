from abc import ABC, abstractmethod
from classes.i_message_client import IMessageClient
from time import time
from asyncio import run
class AbstractPlugin(IMessageClient):
    def __init__(self,id,port):
        self.id = id
        self.ConnectToBroker(port)
        run(self.HeartBeat)
        super().__init__()

    def HeartBeat(self):
        print("heartbeat")
        startTime=time()
        while(time()<startTime+10):
            pass
        self.HeartBeat()

    def ShutDown(self):
        del(self)
        
    def ConnectToBroker(self, port):
        return super().ConnectToBroker(port)
    def SendData(self, topic, msg):
        return super().SendData(topic, msg)
    def OnDataRecieved(self, msg):
        return super().OnDataRecieved(msg)
    