import abc
class ILauncher(metaclass=abc.ABCMeta): #abstract base class
    def LoadConfigFile():
        pass
    def RunPlugins():
        pass
    def RerunPlugin(id: str):
        pass