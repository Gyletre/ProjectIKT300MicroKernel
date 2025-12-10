from PySide6.QtWidgets import QApplication
from login_plugin import PluginWindow


if __name__ == '__main__':
    app = QApplication([])
    plugin = PluginWindow()
    window = plugin.widget
    window.setWindowTitle('User Login Plugin')
    window.resize(300, 100)
    window.show()

    app.exec()
