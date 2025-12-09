import os
import json
from Plugins import ExternalPlugin

class Launcher:
    def __init__(self, folder_path):
        self.folder_path =folder_path

    def run_plugins(self, kernel):
        if not os.path.exists(self.folder_path):
            return
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".json"):
                full_path =  os.path.join(self.folder_path, filename)
                
                
                with open(full_path, 'r')  as f:
                    data= json.load(f)
                    
                    if "FilePath" in data:
                        ExternalPlugin(kernel, data["FilePath"])
