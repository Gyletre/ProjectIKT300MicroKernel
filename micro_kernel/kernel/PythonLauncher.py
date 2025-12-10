from pathlib import Path
import sys
import subprocess
import os

from .ConfigService import ConfigService

path = Path(__file__).resolve().parent.parent.parent / 'shared'
sys.path.insert(0, str(path))

from lib.i_launcher import ILauncher  # type: ignore


def id_generator(start = 1):
    while True:
        yield start
        start += 1


class PythonLauncher(ILauncher):
    def __init__(self, config_service: ConfigService) -> None:
        self.config_service = config_service
        self._id = id_generator()

    def RunPlugin(self, plugin):
        pid = next(self._id)

        plugin_path = str(
            Path(self.config_service.app_config.plugins_directory) / plugin.path
        )
        host = self.config_service.app_config.mqtt.broker_host
        port = self.config_service.app_config.mqtt.broker_port

        try:
            if os.name == "nt":  # Windows
                python_exe = sys.executable

                command = (
                    f'cmd /c start "" "{python_exe}" "{plugin_path}" {pid} {host} {port}'
                )

                p = subprocess.Popen(command, shell=True)

            else:  # Linux / macOS (NOTE: no clue if this works)
                p = subprocess.Popen(
                    [
                        sys.executable,
                        plugin_path,
                        str(pid),
                        host,
                        str(port),
                    ],
                    start_new_session=True,
                )

        except Exception:
            print("Failed to launch plugin:", plugin.name)
            return None

        print("Launched plugin:", plugin.name)
        return pid, plugin, p

    def RunPlugins(self):
        launched_plugins = []
        for plugin in self.config_service.app_config.plugins:
            if plugin.enabled == False: continue
            result = self.RunPlugin(plugin)
            if result is not None:
                launched_plugins.append(result)
        return launched_plugins

