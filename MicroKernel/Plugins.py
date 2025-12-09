import subprocess
import time

class ExternalPlugin:
    def __init__(self, name, path):
        self.name = name
        self.file_path = path
        self.process = None

    def start(self):
        print(f"Starting plugin: {self.name}")
        try:
            self.process = subprocess.Popen(self.file_path)
            print(f"{self.name} started with PID: {self.process.pid}")
        except Exception as e:
            print(f"Error starting {self.name}: {e}")

    def stop(self):
        if self.process:
            print(f"Stopping {self.name}...")
            self.process.terminate()
            self.process = None

    def heart_monitor(self):
        if self.process:
            return self.process.poll() is None # Returns True if running
        return False

    def process(self):
        pass
