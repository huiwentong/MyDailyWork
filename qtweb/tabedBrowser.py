from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import *
from PySide2.QtGui import *
from threading import Thread
from pynput.keyboard import Key, Controller, Listener
import time
from qt_material import apply_stylesheet

def on_press(key):
    print(key)
    print(main.isActiveWindow())
    if main.isActiveWindow():
        if str(key) == r"'\x01'":
            main.aTab.emit(0)
        elif str(key) == r"'\x17'":
            main.aTab.emit(1)


def threadTest():
    with Listener(on_press=on_press) as lis:
        lis.join()


class TabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        QTabWidget.__init__(self, *args, **kwargs)

        self.setMovable(True)
        self.setTabsClosable(True)

        url = QUrl(r"https://www.baidu.com")
        view = HtmlView(self)
        view.load(url)
        print(view.page().title())
        # view.page().setBackgroundColor(QColor().dark(10))
        view.index = self.addTab(view, view.title)
        self.tabCloseRequested.connect(self.on_tab_close)
        view.signal_test.connect(self.change_tex)
        view.signal_icon.connect(self.change_icon)
        # iconsize = QSize(10,10)
        self.setIconSize(QSize(30, 30))
        self.setTabBarAutoHide(True)
        self.tabBar().setExpanding(False)
        self.setTabShape(QTabWidget.Rounded)

    def on_tab_close(self, index):
        self.removeTab(index)
        pass

    def change_tex(self, index, title):
        self.setTabText(index, title)

    def change_icon(self, index, icon):
        self.setTabIcon(index, icon)


class HtmlView(QWebEngineView):
    signal_test = Signal(int, str)
    signal_icon = Signal(int, QIcon)

    def __init__(self, *args, **kwargs):
        QWebEngineView.__init__(self, *args, **kwargs)
        self.index = -1
        self.tab = self.parent()
        self.title = "__main__"
        self.icon = None
        self.titleChanged.connect(self.change_title)
        self.iconChanged.connect(self.change_icon)

    def change_title(self, title):
        # self.signal_test.emit(self.index, title)
        self.tab.setTabText(self.index, title)
        self.title = title
        pass

    def change_icon(self, icon):
        # self.signal_icon.emit(self.index, icon)
        self.tab.setTabIcon(self.index, icon)
        self.icon = icon
        pass

    def createWindow(self, windowType):
        if windowType == QWebEnginePage.WebBrowserTab:
            webView = HtmlView(self.tab)
            webView.index = self.tab.addTab(webView, self.title)
            self.tab.setCurrentIndex(webView.index)

            return webView
        return QWebEngineView.createWindow(self, windowType)


class MainWindow(QMainWindow):
    aTab = Signal(int)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("HWT\'s Cool WebBrowser")
        self.resize(1300, 600)
        self.flag = False
        self.container = QWidget()
        self.tab = TabWidget()
        self.layout_C = QVBoxLayout()
        self.container.setLayout(self.layout_C)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(10, 100)
        self.slider.setValue(100)
        self.slider_name = QLabel('设置不透明度')
        self.topbutton = QPushButton('最前方显示')

        self.op_container = QHBoxLayout()

        self.op_container.addWidget(self.slider_name)
        self.op_container.addWidget(self.slider)
        self.op_container.addWidget(self.topbutton)

        self.layout_C.addLayout(self.op_container)
        self.layout_C.addWidget(self.tab)

        self.setCentralWidget(self.container)
        self.aTab.connect(self.addtab)
        self.slider.valueChanged.connect(self.set_op)
        self.topbutton.clicked.connect(self.top)

    def top(self):
        if not self.flag:
            self.flag = True
            print('top')

            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.topbutton.setText('取消最前显示')
            self.show()
        else:
            self.flag = False
            print('not top')
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.topbutton.setText('最前方显示')
            self.show()

    def set_op(self, value):
        self.setWindowOpacity(value * 0.01)

    def addtab(self, choice):
        if choice == 0:
            url = QUrl(r"http://wiki.ds.com/#recently-worked")
            wiki = HtmlView(self.tab)
            wiki.load(url)
            index = self.tab.currentIndex()
            self.tab.insertTab(index, wiki, 'wiki')
            self.tab.setCurrentIndex(index)
        elif choice == 1:
            index = self.tab.currentIndex()
            self.tab.removeTab(index)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main = MainWindow()
    apply_stylesheet(app, theme='dark_teal.xml')
    main.show()
    t = Thread(target=threadTest)
    t.setDaemon(True)
    t.start()
    sys.exit(app.exec_())
