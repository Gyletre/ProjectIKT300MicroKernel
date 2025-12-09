from abc import ABC, abstractmethod
from classes.i_message_client import IMessageClient
class AbstractPlugin(IMessageClient):
    def __init__(self,id,port):
        self.id = id
        self.ConnectToBroker(port)
        super().__init__()

    def ShutDown(self):
        del(self)
        
    def ConnectToBroker(self, port):
        return super().ConnectToBroker(port)
    def SendData(self, topic, msg):
        return super().SendData(topic, msg)
    def OnDataRecieved(self, msg):
        return super().OnDataRecieved(msg)
    