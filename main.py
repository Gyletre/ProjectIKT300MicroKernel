import threading

from micro_kernel import Kernel


if __name__ == '__main__':
    kernel = Kernel()

    threading.Event().wait()