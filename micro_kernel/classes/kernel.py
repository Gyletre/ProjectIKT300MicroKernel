from classes.i_launcher import ILauncher

class Kernel:
    def __init__(self, l: ILauncher):
        self.launcher = l
    def Startup(self):
        self.pluginIDs = self.launcher.RunPlugins()
    def ShutDownAll(self):
        pass
    def __del__(self):
        self.ShutDownAll()
        