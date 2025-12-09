from abc import ABC, abstractmethod

class IMessageClient(ABC):
    @abstractmethod
    def ConnectToBroker(self, port:int):
        pass
    @abstractmethod
    def OnDataRecieved(self, msg: str):
        pass
    @abstractmethod
    def SendData(self, topic:str, msg:str):
        pass