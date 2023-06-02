import sys
import random
from PySide2 import QtWidgets
from PySide2.QtWidgets import QMainWindow
from pyside2_master.mainwindow_ui import Ui_Form


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.hello = ["hallo welt", "hello world", "你好世界"]
        self.pushButton.clicked.connect(self.magic)
        with open("testQtGui", "r", encoding="UTF-8") as qss:
            self.setStyleSheet(qss.read())

    def magic(self):
        self.label.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
