from Kernel import Kernel
from Plugins import TestPlugin, GUIPlugin
from Launcher import Launcher
import os

def main():
    kernel = Kernel()
    
    # Sett opp launcher
    config_path = os.path.join(os.getcwd(), "PluginConfigs")
    launcher = Launcher(config_path)
    kernel.set_launcher(launcher)

    # Legg til interne plugins
    TestPlugin(kernel)
    GUIPlugin(kernel)

    # Kjør
    kernel.run()

if __name__ == "__main__":
    main()
