"""topics: accmgr/*"""

import json
from pathlib import Path
import sys
import time
import os
import threading

from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget
)
from PySide6.QtCore import Qt

path = Path(__file__).resolve().parent.parent.parent / 'shared'
sys.path.insert(0, str(path))

from lib import AbstractPlugin, MQTTMessage  # type: ignore


class LoginPage(QWidget):
    def __init__(self, on_login):
        super().__init__()

        self.on_login = on_login

        self.setWindowTitle('User Login')
        self.resize(300, 150)

        self.user_label = QLabel('Username:')
        self.user_input = QLineEdit()

        self.pass_label = QLabel('Password')
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton('Log in')
        self.message = QLabel('')
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()

        user_layout = QHBoxLayout()
        user_layout.addWidget(self.user_label)
        user_layout.addWidget(self.user_input)

        pass_layout = QHBoxLayout()
        pass_layout.addWidget(self.pass_label)
        pass_layout.addWidget(self.pass_input)

        layout.addLayout(user_layout)
        layout.addLayout(pass_layout)
        layout.addWidget(self.login_button)
        layout.addWidget(self.message)

        self.setLayout(layout)

        self.user_input.returnPressed.connect(self.pass_input.setFocus)
        self.pass_input.returnPressed.connect(self.login_button.click)
        self.login_button.clicked.connect(self.try_login)

    def try_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        self.user_input.clear()
        self.pass_input.clear()

        if username and password:
            self.message.setText('')
            self.user_input.setFocus()
            self.on_login(username, password)
        else:
            self.message.setText('Invalid username or password!')
            self.user_input.setFocus()


class LogoutPage(QWidget):
    def __init__(self, on_logout):
        super().__init__()

        self.label = QLabel('You are logged in.')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logout_button = QPushButton('Log out')

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

        self.logout_button.clicked.connect(on_logout)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.logout_button.click()


class PluginWindow(AbstractPlugin):
    def __init__(self):
        super().__init__()

        self.username = None
        self.password = None

        # The plugin is NOT a Qt widget now — it contains one
        self.widget = QStackedWidget()

        self.login_page = LoginPage(self.show_logout_page)
        self.logout_page = LogoutPage(self.show_login_page)

        self.widget.addWidget(self.login_page)
        self.widget.addWidget(self.logout_page)

        self.widget.setCurrentIndex(0)

        time.sleep(1)
        self._Subscribe('kernel/heartbeat')

    def show_login_page(self):
        if self.username is not None:
            self._SendData('accmgr/user', json.dumps({
                'type': 'UserLoggedOutEvent',
                'payload': {'username': self.username}
            }))
        self.widget.setCurrentIndex(0)

    def show_logout_page(self, username, password):
        self.username = username
        self.password = password
        self._SendData('accmgr/user', json.dumps({
            'type': 'UserLoggedInEvent',
            'payload': {'username': username, 'password': password}
        }))
        self.widget.setCurrentIndex(1)

    def _OnDataReceived(self, client, userdata, message: MQTTMessage):
        if message.topic == 'kernel/heartbeat':
            self.last_kernel_heartbeat = time.time()

if __name__ == '__main__':
    app = QApplication([])
    plugin = PluginWindow()
    window = plugin.widget
    window.setWindowTitle('User Login Plugin')
    window.resize(300, 100)
    window.show()

    app.exec()
