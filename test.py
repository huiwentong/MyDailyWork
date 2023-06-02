import sys

from PySide2.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide2 import QtCore, QtWidgets, QtGui, QtUiTools
from stacked_ui import Ui_MainWindow
from PySide2.QtCore import QDir


class myMain(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(myMain, self).__init__()
        self.setupUi(self)
        self.resize(500, 500)
        self.setWindowTitle('this is huiwentongs test' )

        self.button = QtWidgets.QPushButton('show_status_bar')
        self.button.clicked.connect(self.showState)
        self.button2 = QtWidgets.QPushButton()
        self.button2.setObjectName('button2')
        self.button2.setStyleSheet('#button2{border-image:url(connector_icon_connected_a.png);}')
        self.button2.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.button2.setMinimumSize(100, 100)


        self.button2.clicked.connect(self.openSub)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.stackedWidget)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.button2)
        self.centralwidget.setLayout(self.layout)
        self.w1 = QtWidgets.QWidget()
        self.label1 = QtWidgets.QLabel('asdasdasdasd', self.w1)
        self.manu = QtWidgets.QMenu()
        self.manuBar = QtWidgets.QMenuBar()
        self.w2 = QtWidgets.QWidget()
        self.label2 = QtWidgets.QLabel('W2W2asdasda', self.w2)

        self.w3 = QtWidgets.QWidget()
        self.label3 = QtWidgets.QLabel('W3W3asdasdas', self.w3)

        self.stackedWidget.insertWidget(0, self.w1)
        self.stackedWidget.addWidget(self.w2)
        self.stackedWidget.addWidget(self.w3)
        self.stackedWidget.removeWidget(self.page)
        self.stackedWidget.removeWidget(self.page_2)
        self.stackedWidget.setCurrentWidget(self.w1)
        self.stackedWidget.setCurrentIndex(2)


        self.statusLabel = QtWidgets.QLabel('asdasdasdasdasdasdasdasdasdasdasd')
        # self.statusbar.addWidget(self.statusLabel)

    # @QtCore.Slot()
    def showState(self):
        print('call the show')
        self.statusbar.showMessage('asdasdasd')

    def openSub(self):
        file, _ = QFileDialog.getOpenFileName(self.button, "打开文件", QDir.currentPath(), "视频文件(*.mp4 *.avi);;所有文件(*)")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = myMain()
    window.show()
    sys.exit(app.exec_())
