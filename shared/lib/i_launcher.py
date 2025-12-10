from abc import ABC, abstractmethod


class ILauncher(ABC):  # abstract base class    
    @abstractmethod
    def RunPlugins(self):
        pass