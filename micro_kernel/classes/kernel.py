from classes.i_launcher import ILauncher
from classes.i_message_client import IMessageClient
class Kernel(IMessageClient):
    def __init__(self, l: ILauncher,port:int):
        self.launcher: ILauncher = l
        self.__Startup(port)
    def __Startup(self,port):
        self.ConnectToBroker(port)
        self.pluginIDs = self.launcher.RunPlugins()
    def ShutDownAll(self):
        # Send shut down message to all plugins
        pass
    def __del__(self):
        self.ShutDownAll()

    def SendData(self, topic, msg):
        return super().SendData(topic, msg)
    def OnDataRecieved(self, msg):
        return super().OnDataRecieved(msg)
    def ConnectToBroker(self, port):
        return super().ConnectToBroker(port)

        