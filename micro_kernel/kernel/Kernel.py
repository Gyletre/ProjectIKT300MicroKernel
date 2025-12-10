from pathlib import Path
from typing import Optional
import sys
import time
import json
import threading
from collections import defaultdict

from .ConfigService import ConfigService
from .PythonLauncher import PythonLauncher

path = Path(__file__).resolve().parent.parent.parent / 'shared'
sys.path.insert(0, str(path))

from lib import MQTTMessage, MQTTClientConfig, MQTTClient  # type: ignore


class Kernel(MQTTClient):
    def __init__(self, config_path: Optional[str] = None, launcher = PythonLauncher) -> None:
        if config_path is None:
            config_path = str(Path(__file__).resolve().parent.parent / 'configs/app_config.json')
        
        self.config_service = ConfigService.load_from_json(config_path)

        super().__init__(MQTTClientConfig(-1, self.config_service.app_config.mqtt.broker_host, self.config_service.app_config.mqtt.broker_port))

        self.launcher = launcher(self.config_service)

        self.plugins = dict()
        for pid, plugin, process in self.launcher.RunPlugins():
            self.plugins[pid] = (plugin, process)

        self.plugin_status = defaultdict(lambda: time.time())

        time.sleep(1)
        self._Subscribe('plugins/morgue')
        self._Subscribe('heartbeat/#')

        t = threading.Thread(target=self._heartbeat, daemon=True)
        t.start()

        self.status_lock = threading.Lock()

    def _heartbeat(self):
        while True:
            self._SendData('kernel/heartbeat', "I'm alive!")
            for pid, (plugin, process) in list(self.plugins.items()):
                if time.time() - self.plugin_status[pid] > self.KEEPALIVE:
                    del self.plugins[pid]
                    process.kill()
                    if plugin.restart_on_failure:
                        result = self.launcher.RunPlugin(plugin)
                        if result is None: continue
                        pid, plugin, process = result
                        self.plugins[pid] = (plugin, process)
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
        if message.topic.startswith('heartbeat/'):
            # print('heartbeat:', message.topic)
            pid = int(message.topic.split('/')[1])
            self.plugin_status[pid] = time.time()