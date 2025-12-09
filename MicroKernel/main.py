import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MicroKernel.Kernel import Kernel
from MicroKernel.Launcher import Launcher

if __name__ == "__main__":
    kernel = Kernel()
    launcher = Launcher(kernel)
    
    launcher.load_plugins()
    kernel.run()
