import sys
import pyperclip
import logging
import time
from pynput import keyboard
from pynput.keyboard import Controller
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ClipboardTypeApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray_icon = QSystemTrayIcon(QIcon("logo.ico"), parent=self.app)
        self.tray_icon.setToolTip("Clipboard Type App")

        self.menu = QMenu()

        self.start_action = QAction("Start", self.app)
        self.start_action.triggered.connect(self.start_listening)
        self.menu.addAction(self.start_action)

        self.stop_action = QAction("Stop", self.app)
        self.stop_action.triggered.connect(self.stop_listening)
        self.menu.addAction(self.stop_action)

        self.exit_action = QAction("Exit", self.app)
        self.exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()

        self.is_listening = False
        self.listener = None
        self.keyboard_controller = Controller()

        # Автоматически запускаем слушатель при старте программы
        self.start_listening()

    def start_listening(self):
        if not self.is_listening:
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            self.is_listening = True
            logging.info("Listening started")
            self.tray_icon.showMessage("Clipboard Type App", "Listening started", QSystemTrayIcon.Information, 2000)

    def stop_listening(self):
        if self.is_listening and self.listener:
            self.listener.stop()
            self.is_listening = False
            logging.info("Listening stopped")
            self.tray_icon.showMessage("Clipboard Type App", "Listening stopped", QSystemTrayIcon.Information, 2000)

    def on_press(self, key):
        try:
            # Проверяем, нажата ли клавиша Numpad Enter
            if key == keyboard.Key.enter:
                logging.info("Numpad Enter pressed")
                self.type_clipboard_content()
        except AttributeError:
            pass

    def type_clipboard_content(self):
        logging.info("Hotkey pressed")  # Логирование для проверки срабатывания
        content = pyperclip.paste()  # Получаем текст из буфера обмена
        if content:
            logging.info(f"Typing content: {content}")
            for char in content:
                self.keyboard_controller.type(char)  # Печатаем каждый символ по одному
                time.sleep(0.04)  # Задержка 0.04 секунды между символами
        else:
            logging.warning("Clipboard is empty")

    def exit_app(self):
        self.stop_listening()
        self.tray_icon.hide()
        logging.info("Exiting application")
        QCoreApplication.exit()

    def run(self):
        logging.info("Application started")
        self.app.exec_()

if __name__ == "__main__":
    app = ClipboardTypeApp()
    app.run()
