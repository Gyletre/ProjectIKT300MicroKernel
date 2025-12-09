import os
import json
from MicroKernel.Plugins import ExternalPlugin

class Launcher:
    def __init__(self, kernel):
        self.kernel = kernel
        self.config_folder = os.path.join(os.path.dirname(__file__), "PluginConfigs")

    def load_plugins(self):
        if not os.path.exists(self.config_folder):
            print(f"Config folder not found: {self.config_folder}")
            os.makedirs(self.config_folder, exist_ok=True)
            return

        for filename in os.listdir(self.config_folder):
            if filename.endswith(".json"):
                filepath = os.path.join(self.config_folder, filename)
                try:
                    with open(filepath, "r") as f:
                        config = json.load(f)
                        
                        name = config.get("name")
                        path = config.get("path")
                        
                        if name and path:
                            plugin = ExternalPlugin(name, path)
                            self.kernel.add_plugin(plugin)
                            print(f"Registered plugin: {name}")
                except Exception as e:
                    print(f"Failed to load config {filename}: {e}")
