from PySide2.QtWidgets import QApplication, QMainWindow
from ui_main import Ui_MainWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_MainWindow()
        # 初始化界面
        self.ui.setupUi(self)

        # 使用界面定义的控件，也是从ui里面访问
        self.ui.webview.load('http://www.python3.vip/')

app = QApplication([])
mainw = MainWindow()
mainw.show()
app.exec_()