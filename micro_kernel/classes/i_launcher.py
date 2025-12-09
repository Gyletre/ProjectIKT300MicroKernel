from abc import ABC, abstractmethod

class ILauncher(ABC):
    @abstractmethod
    def LoadConfigFile(self):
        pass
    @abstractmethod
    def RunPlugins(self):
        pass
    @abstractmethod
    def RerunPlugin(self, id: str):
        pass