import time

class Kernel:
    def __init__(self):
        self.running = True
        self.plugins = []
        self.fps = 60
        self.launcher =None

    def set_launcher(self, launcher):
        self.launcher = launcher
    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def restart_plugin(self, plugin):
        plugin.stop()
        plugin.start()
    def run(self):
        print("Greetings, Universe")
        
        if self.launcher:
            self.launcher.run_plugins(self)
        for plugin in self.plugins:
            plugin.start()

        old_time = time.time()
        time_to_run = 300

        while self.running:
            current_time = time.time()
            time.sleep(1/self.fps)

            for i in range(len(self.plugins) -  1, -1, -1):
                plugin = self.plugins[i]
                if plugin.heart_monitor() == 1:
                    plugin.process()
                else:
                    print("Plugin didnt work")
                    self.restart_plugin(plugin)
                    if plugin.heart_monitor() ==   1:
                        print("Plugin restarted")
                    else:
                        plugin.stop()
                        self.plugins.pop(i)
            
            time_to_run -= 1
            if time_to_run <  0:
                self.running =  False
        
        self.shutdown()
    def shutdown(self):
        for plugin in self.plugins:
            plugin.stop()
        self.plugins.clear()
