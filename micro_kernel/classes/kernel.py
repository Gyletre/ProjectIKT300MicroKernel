from i_launcher import ILauncher
from i_message_client import IMessageClient
from mqtt_client import MQTTClient,MQTTClientConfig
class Kernel(MQTTClient):
    def __init__(self, l: ILauncher,brokerIP,port:int):
        super().__init__(MQTTClientConfig(-1,brokerIP,port))
        self.launcher: ILauncher = l
        self.__Startup()
    def __Startup(self):
        self._ConnectToBroker()
        self.pluginIDs = self.launcher.RunPlugins()
    def ShutDownAll(self):
        self._SendData("status/shutdown",'\{"program":1\}')

        pass
    def __del__(self):
        self.ShutDownAll()

        