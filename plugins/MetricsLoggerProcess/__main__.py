from pathlib import Path
import sys
import json
import os
import threading
import time

path = Path(__file__).resolve().parent.parent.parent / 'shared'
sys.path.insert(0, str(path))

from lib import AbstractPlugin, MQTTMessage  # type: ignore


class MetricsLoggerProcess(AbstractPlugin):
    def __init__(self):
        super().__init__()

        self.messages = 0

        time.sleep(1)
        self._Subscribe('kernel/heartbeat')
        self._Subscribe('accmgr/user')
        self._Subscribe('dataprocessor/events')  # this one is unused

        self.last_kernel_heartbeat = time.time()
        t = threading.Thread(target=self.watchdog, daemon=True)
        t.start()

    def _OnUserLoggedInEvent(self, payload):
        self.messages += 1
        print(f'[{self.messages}]', payload)

    def _OnDataProcessedEvent(self, payload):
        self.messages += 1
        print(f'[{self.messages}]', payload)

    def _OnDataReceived(self, client, userdata, message: MQTTMessage):
        if message.topic == 'kernel/heartbeat':
            self.last_kernel_heartbeat = time.time()
        if message.topic == 'accmgr/user':
            payload = json.loads(message.payload)
            if payload['type'] == 'UserLoggedInEvent':
                self._OnUserLoggedInEvent(payload)
        if message.topic == 'dataprocessor/events':
            payload = json.loads(message.payload)
            if payload['type'] == 'DataProcessedEvent':
                self._OnDataProcessedEvent(payload)

    def watchdog(self):
        while True:
            if time.time() - self.last_kernel_heartbeat > self.NO_HEARTBEAT_EXIT:
                os._exit(0)
            time.sleep(1)


if __name__ == '__main__':
    plugin = MetricsLoggerProcess()
    threading.Event().wait()