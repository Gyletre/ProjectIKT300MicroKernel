import subprocess
import os

class Plugin:
    def __init__(self, kernel):
        self.kernel = kernel
        self.kernel.add_plugin(self)

    def start(self):
        pass

    def stop(self):
        pass

    def heart_monitor(self):
        return 1

    def process(self):
        pass

class TestPlugin(Plugin):
    def start(self):
        print("TestPlugin startet")

    def stop(self):
        print("TestPlugin stoppet")

    def process(self):
        print("Testing")

class GUIPlugin(Plugin):
    def start(self):
        print("GUIPlugin startet")

    def process(self):
        pass

class ExternalPlugin(Plugin):
    def __init__(self, kernel, path):
        super().__init__(kernel)
        self.file_path = path
        self.process_obj = None

    def start(self):
        try:
            self.process_obj = subprocess.Popen(self.file_path)
            print("Startet ekstern: " + self.file_path)
        except:
            print("Klarte ikke starte: " + self.file_path)

    def stop(self):
        if self.process_obj:
            self.process_obj.terminate()
            print("Stoppet ekstern: " + self.file_path)

    def heart_monitor(self):
        if self.process_obj is None:
            return 0
        if self.process_obj.poll() is not None:
            return 0 # Død
        return 1 # Lever
