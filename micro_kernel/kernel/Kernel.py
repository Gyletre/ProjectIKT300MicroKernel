from micro_kernel.kernel import PythonLauncher


class Kernel:
    def __init__(self, pythonLauncher: PythonLauncher):
        self._python_launcher = pythonLauncher
        