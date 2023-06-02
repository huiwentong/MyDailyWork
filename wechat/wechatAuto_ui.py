# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'wechatAuto.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(400, 638)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton_main_start = QPushButton(self.centralwidget)
        self.pushButton_main_start.setObjectName(u"pushButton_main_start")
        self.pushButton_main_start.setGeometry(QRect(140, 520, 141, 41))
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 10, 361, 131))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_myname = QLabel(self.widget)
        self.label_myname.setObjectName(u"label_myname")

        self.horizontalLayout.addWidget(self.label_myname)

        self.textEdit_myname = QTextEdit(self.widget)
        self.textEdit_myname.setObjectName(u"textEdit_myname")

        self.horizontalLayout.addWidget(self.textEdit_myname)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_Tarname = QLabel(self.widget)
        self.label_Tarname.setObjectName(u"label_Tarname")

        self.horizontalLayout_2.addWidget(self.label_Tarname)

        self.textEdit_Tarname = QTextEdit(self.widget)
        self.textEdit_Tarname.setObjectName(u"textEdit_Tarname")

        self.horizontalLayout_2.addWidget(self.textEdit_Tarname)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_zaoan = QLabel(self.widget)
        self.label_zaoan.setObjectName(u"label_zaoan")

        self.horizontalLayout_3.addWidget(self.label_zaoan)

        self.textEdit_zaoan = QTextEdit(self.widget)
        self.textEdit_zaoan.setObjectName(u"textEdit_zaoan")

        self.horizontalLayout_3.addWidget(self.textEdit_zaoan)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_gongzuoshijian = QLabel(self.widget)
        self.label_gongzuoshijian.setObjectName(u"label_gongzuoshijian")

        self.horizontalLayout_4.addWidget(self.label_gongzuoshijian)

        self.spinBox_gongzuoshijian_start = QSpinBox(self.widget)
        self.spinBox_gongzuoshijian_start.setObjectName(u"spinBox_gongzuoshijian_start")

        self.horizontalLayout_4.addWidget(self.spinBox_gongzuoshijian_start)

        self.spinBox_gongzuoshijian_end = QSpinBox(self.widget)
        self.spinBox_gongzuoshijian_end.setObjectName(u"spinBox_gongzuoshijian_end")

        self.horizontalLayout_4.addWidget(self.spinBox_gongzuoshijian_end)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_xiabanshijian = QLabel(self.widget)
        self.label_xiabanshijian.setObjectName(u"label_xiabanshijian")

        self.horizontalLayout_5.addWidget(self.label_xiabanshijian)

        self.spinBox_xiabanshijian_start = QSpinBox(self.widget)
        self.spinBox_xiabanshijian_start.setObjectName(u"spinBox_xiabanshijian_start")

        self.horizontalLayout_5.addWidget(self.spinBox_xiabanshijian_start)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.widget1 = QWidget(self.centralwidget)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(20, 150, 361, 361))
        self.verticalLayout_2 = QVBoxLayout(self.widget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_zaoan_content = QLabel(self.widget1)
        self.label_zaoan_content.setObjectName(u"label_zaoan_content")

        self.verticalLayout_3.addWidget(self.label_zaoan_content)

        self.checkBox_zaoan_content = QCheckBox(self.widget1)
        self.checkBox_zaoan_content.setObjectName(u"checkBox_zaoan_content")

        self.verticalLayout_3.addWidget(self.checkBox_zaoan_content)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)

        self.plainTextEdit_zaoan_content = QPlainTextEdit(self.widget1)
        self.plainTextEdit_zaoan_content.setObjectName(u"plainTextEdit_zaoan_content")

        self.horizontalLayout_6.addWidget(self.plainTextEdit_zaoan_content)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_gongzuo_content = QLabel(self.widget1)
        self.label_gongzuo_content.setObjectName(u"label_gongzuo_content")

        self.verticalLayout_5.addWidget(self.label_gongzuo_content)

        self.checkBox_gongzuo_content = QCheckBox(self.widget1)
        self.checkBox_gongzuo_content.setObjectName(u"checkBox_gongzuo_content")

        self.verticalLayout_5.addWidget(self.checkBox_gongzuo_content)


        self.horizontalLayout_8.addLayout(self.verticalLayout_5)

        self.plainTextEdit_gongzuo_content = QPlainTextEdit(self.widget1)
        self.plainTextEdit_gongzuo_content.setObjectName(u"plainTextEdit_gongzuo_content")

        self.horizontalLayout_8.addWidget(self.plainTextEdit_gongzuo_content)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_xiaban_content = QLabel(self.widget1)
        self.label_xiaban_content.setObjectName(u"label_xiaban_content")

        self.verticalLayout_4.addWidget(self.label_xiaban_content)

        self.checkBox__xiaban_content = QCheckBox(self.widget1)
        self.checkBox__xiaban_content.setObjectName(u"checkBox__xiaban_content")

        self.verticalLayout_4.addWidget(self.checkBox__xiaban_content)


        self.horizontalLayout_7.addLayout(self.verticalLayout_4)

        self.plainTextEdit_xiaban_content = QPlainTextEdit(self.widget1)
        self.plainTextEdit_xiaban_content.setObjectName(u"plainTextEdit_xiaban_content")

        self.horizontalLayout_7.addWidget(self.plainTextEdit_xiaban_content)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_main_start.setText(QCoreApplication.translate("MainWindow", u"\u70b9\u51fb\u5f00\u59cb\u5faa\u73af", None))
        self.label_myname.setText(QCoreApplication.translate("MainWindow", u"\u6211\u7684\u6635\u79f0", None))
        self.label_Tarname.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u6807\u6635\u79f0", None))
        self.label_zaoan.setText(QCoreApplication.translate("MainWindow", u"\u65e9\u5b89\u65f6\u95f4", None))
        self.textEdit_zaoan.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u4f8b\u5982  09:00", None))
        self.label_gongzuoshijian.setText(QCoreApplication.translate("MainWindow", u"\u5de5\u4f5c\u65f6\u95f4\u6bb5", None))
        self.label_xiabanshijian.setText(QCoreApplication.translate("MainWindow", u"\u51e0\u70b9\u4e0b\u73ed", None))
        self.label_zaoan_content.setText(QCoreApplication.translate("MainWindow", u"\u65e9\u5b89\u65f6\u95ee\u5019\u8bed", None))
        self.checkBox_zaoan_content.setText(QCoreApplication.translate("MainWindow", u"\u4e0d\u8986\u76d6\u9ed8\u8ba4\u6570\u503c", None))
        self.label_gongzuo_content.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u73ed\u65f6\u95f4\u56de\u590d", None))
        self.checkBox_gongzuo_content.setText(QCoreApplication.translate("MainWindow", u"\u4e0d\u8986\u76d6\u9ed8\u8ba4\u6570\u503c", None))
        self.label_xiaban_content.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u73ed\u65f6\u95f4\u56de\u590d", None))
        self.checkBox__xiaban_content.setText(QCoreApplication.translate("MainWindow", u"\u4e0d\u8986\u76d6\u9ed8\u8ba4\u6570\u503c", None))
    # retranslateUi

