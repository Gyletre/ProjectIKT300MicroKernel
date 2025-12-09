from classes.i_launcher import ILauncher
from os.path import dirname
import subprocess

#Example of launcher
class EXELauncher(ILauncher):
    def __init__(self, port):
        self.exeConfigPath = dirname(__file__) + "/exe_config.txt"
        self.port = port
        super().__init__()

    def LoadConfigFile(self):
        self.plugins = {}
        with open(self.exeConfigPath, "r") as file:
            for line in file:
                id, path = line.split(" ")
                self.plugins[id] = dirname(__file__) + path

    def RunPlugins(self):
        for id, path in self.plugins:
            subprocess.Popen([
                "cmd", "/c", "start", "cmd", "/c", f"python -m {path} {id} {self.port}"
                ])
            pass

    def RerunPlugin(self, id):
        return super().RerunPlugin(id)

