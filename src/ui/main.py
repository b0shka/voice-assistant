import sys
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject


class Assistant(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.commands = ["Мои уведомления", "Сообщения в Телеграм"]


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    assistant = Assistant()

    engine.rootContext().setContextProperty("assistant", assistant)
    engine.rootContext().setContextProperty("commands", assistant.commands)

    engine.load("main.qml")
    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
