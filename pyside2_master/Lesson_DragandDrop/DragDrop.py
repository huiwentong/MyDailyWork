# -*- coding: utf-8 -*-

"""
ZetCode PySide tutorial

This is a simple drag and
drop example.

author: Jan Bodnar
website: zetcode.com
last edited: August 2011
"""

import sys
from PySide2 import QtGui, QtCore, QtWidgets

class Button(QtWidgets.QPushButton): # 定义Button类,以实现拖拽操作

    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e): # 重写 拖 函数,定义好我们要接受的数据类型

        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e): # 重写 放 函数,具体实现一个改变按钮的文本的操作
        self.setText(e.mimeData().text())


class Example(QtWidgets.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        qe = QtWidgets.QLineEdit('', self)
        qe.setDragEnabled(True)
        qe.move(30, 65)

        button = Button("Button", self)
        button.move(190, 65)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Simple Drag & Drop')
        self.show()

def main():#实现将行编辑器中的文本拖拽到按钮上，我们必须重写一些方法，所以我们在继承QtGui.QPushButton的基础上创造我们自己的BUTTON类

    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())





class Button2(QtWidgets.QPushButton):

    def __init__(self, title, parent):
        super(Button2, self).__init__(title, parent)
        self.pix = QtGui.QPixmap('E:\\MyGit\\MyDailyWork\\pyside2_master\\Lesson_DragandDrop\\test.png')

    def mouseMoveEvent(self, e):

        if e.buttons() != QtCore.Qt.RightButton:
            return
        mimeData = QtCore.QMimeData()
        print(self.rect().topLeft())
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(self.pix)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.start(QtCore.Qt.MoveAction)


    def mousePressEvent(self, e):

        QtWidgets.QPushButton.mousePressEvent(self, e)
        if e.button() == QtCore.Qt.LeftButton:
            print('press')


class Example2(QtWidgets.QWidget):

    def __init__(self):
        super(Example2, self).__init__()

        self.initUI()

    def initUI(self):

        self.setAcceptDrops(True)

        self.btn = Button2('Button', self)
        self.btn.move(100, 65)
        # self.label = QtWidgets.QLabel(self)
        # self.label.resize(50, 50)
        # self.label.setPixmap(QtGui.QPixmap('E:\\MyGit\\MyDailyWork\\pyside2_master\\Lesson_DragandDrop\\test.png'))
        # self.label.move(100, 200)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Click or move')
        self.show()

    def dragEnterEvent(self, e):

        e.accept()

    def dropEvent(self, e):

        position = e.pos()
        self.btn.move(position)

        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()

def main2():#如何拖拽一个button，在本示例中，点击左键会显示 ‘press’，按压住右键可以拖拽按钮

    app = QtWidgets.QApplication(sys.argv)
    ex = Example2()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main2()