from classes.i_launcher import ILauncher
from classes.i_message_client import IMessageClient
from classes.mqtt_client import MQTTClient,MQTTClientConfig
class Kernel(MQTTClient):
    def __init__(self, l: ILauncher,brokerIP,port:int):
        self.launcher: ILauncher = l
        self.__Startup(port)
        super().__init__(MQTTClientConfig(-1,brokerIP,port))
    def __Startup(self):
        self._ConnectToBroker()
        self.pluginIDs = self.launcher.RunPlugins()
    def ShutDownAll(self):
        self._SendData("status/shutdown",'\{"program":1\}')

        pass
    def __del__(self):
        self.ShutDownAll()

        