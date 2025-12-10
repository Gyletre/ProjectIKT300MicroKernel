from abc import ABC, abstractmethod


class IMessageClient(ABC):
    @abstractmethod
    def _ConnectToBroker(self, port:int):
        pass
    
    @abstractmethod
    def _OnDataReceived(self, msg: str):
        pass
    
    @abstractmethod
    def _SendData(self, topic:str, msg:str):
        pass