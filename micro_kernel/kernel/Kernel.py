from pathlib import Path
from typing import Optional
import sys
import time
import json
import threading

from .ConfigService import ConfigService
from .PythonLauncher import PythonLauncher

path = Path(__file__).resolve().parent.parent.parent / 'shared'
sys.path.insert(0, str(path))

from lib import AbstractPlugin, MQTTMessage, MQTTClientConfig  # type: ignore


class Kernel(AbstractPlugin):
    def __init__(self, config_path: Optional[str] = None) -> None:
        if config_path is None:
            config_path = str(Path(__file__).resolve().parent.parent / 'configs/app_config.json')
        
        self.config_service = ConfigService.load_from_json(config_path)

        super().__init__(MQTTClientConfig(-1, self.config_service.app_config.mqtt.broker_host, self.config_service.app_config.mqtt.broker_port))

        self.launcher = PythonLauncher(self.config_service)

        self.plugins = dict()
        for pid, plugin, process in self.launcher.RunPlugins():
            self.plugins[pid] = (plugin, process)

        time.sleep(1)
        self._Subscribe('accmgr/#')
        self._Subscribe('plugins/morgue')

        t = threading.Thread(target=self._heartbeat, daemon=True)
        t.start()

    def _heartbeat(self):
        while True:
            self._SendData('kernel/heartbeat', "I'm alive!")
            time.sleep(1)

    def _OnDataReceived(self, client, userdata, message: MQTTMessage):
        if message.topic == 'plugins/morgue':
            payload = json.loads(message.payload)
            pid = payload['payload']['id']
            if not self.plugins[pid]: return
            print('plugin died:', pid)
            plugin = self.plugins[pid][0]
            del self.plugins[pid]
            if plugin.restart_on_failure:
                result = self.launcher.RunPlugin(plugin)
                if result is None: return
                pid, plugin, process = result
                self.plugins[pid] = (plugin, process)