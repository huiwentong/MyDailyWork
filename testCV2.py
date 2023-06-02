import os
from glob import glob
import sys

from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication
from PySide2.QtCore import QDir, QTimer, QSize
from PySide2.QtGui import QPixmap, QImage
from untitled_ui import Ui_MainWindow
import cv2 as cv


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.f_type = 0

    def window_init(self):
        size = self.frameSize().width()
        self.resize(size, 750)
        self.label.setText("请打开")
        self.asd.setTitle("主菜单")
        self.actionasd.setText("打开图片")
        self.actionasd_2.setText("打开视频")

        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.actionasd.triggered.connect(ImgConfig_init)
        # self.actionasd_2.triggered.connect(VdoConfig_init)

        self.label.setScaledContents(True)


class ImgConfig:
    def __init__(self):
        self.files, self.full_file_name = openImg()
        if not self.files:
            return
        self.n = len(self.files)

        window.pushButton_2.setEnabled(True)
        window.pushButton_3.setEnabled(True)

        window.pushButton.setText("暂停")
        window.pushButton_2.setText("上一个")
        window.pushButton_3.setText("下一个")

        file_names = []
        for c in range(self.n):
            (dir_name, full_file_name) = os.path.split(self.files[c])
            file_names.append(full_file_name)
        self.counter = file_names.index(self.full_file_name)

        direct_show_image(self.files[self.counter])
        window.pushButton_2.clicked.connect(self.last_img)
        window.pushButton_3.clicked.connect(self.next_img)
    def last_img(self):
        if self.counter > 0:
            self.counter -= 1
        else:
            self.counter = self.n-1
        direct_show_image(self.files[self.counter])
    def next_img(self):
        if self.counter <self.n-1:
            self.counter += 1
        else:
            self.counter = 0
        direct_show_image(self.files[self.counter])


def ImgConfig_init():
    window.f_type = ImgConfig()


def openImg():
    default_path = r"C:\Users\huiwentong\Desktop"
    file_dir, _ = QFileDialog.getOpenFileName(window.label, "打开文件", default_path, "图片(*.jpg *.png *.bmp);;所有文件(*);;mp4(*.mp4)")
    if not file_dir:
        QMessageBox.warning(window.label, "警告", "打不开可咋整", QMessageBox.Ok)
        return None, None
    QMessageBox.warning(window.label, "提示", "导入文件成功", QMessageBox.Ok)
    (dir_name, full_file_name) = os.path.split(file_dir)
    (file_name, file_type) = os.path.splitext(full_file_name)
    files = glob(os.path.join(dir_name, "*{}".format(file_type)))
    return files, full_file_name


def direct_show_image(img):
    pixmap = QPixmap(img)
    pixmap = pixmap.scaled(window.label.size() - QSize(2, 2))
    window.label.setPixmap(pixmap)
    (f_dir, f_name) = os.path.split(img)
    window.statusbar.showMessage("文件名：{}".format(f_name))

def open_video():
    default_path = r"C:\Users\huiwentong\Desktop"
    file_dir, _ = QFileDialog.getOpenFileName(window.label, "打开视频", default_path, "视频文件(*.mp4 *.avi );;所有文件(*)")
    if not file_dir:
        QMessageBox.warning(window.label, "警告", "打开视频失败", QMessageBox.Ok)
        return None
    print("读入成功")
    return file_dir

class VdoConfig:
    def __init__(self):
        window.pushButton.setEnabled(False)
        window.pushButton_2.setEnabled(False)
        window.pushButton_3.setEnabled(False)
        self.file = open_video()
        if not self.file:
            return
        window.label.setText("正在读取请稍后...")

        self.V_timer = QTimer()
        self.cap = cv.VideoCapture(self.file)
        if not self.cap:
            print("打开视频失败")
            return
        self.fps = self.cap.get(cv.CAP_PROP_FPS)
        self.total_f = self.cap.get(cv.CAP_PROP_FRAME_COUNT)
        self.current_f = self.cap.get(cv.CAP_PROP_POS_FRAMES)
        self.V_timer.start(int(1000/self.fps))
        print("FPS:".format(self.fps))

        window.pushButton_2.setEnabled(True)
        window.pushButton_3.setEnabled(True)
        window.pushButton.setEnabled(True)
        window.pushButton_2.setText("快退")
        window.pushButton_3.setText("快进")
        window.pushButton.setText("暂停")

        self.V_timer.timeout.connect(self.show_pic)

        window.pushButton.clicked.connect(self.go_pause)
        window.pushButton_2.clicked.connect(lambda: self.last_img(True))
        window.pushButton_3.clicked.connect(lambda: self.last_img(True))
        window.pushButton_2.pressed.connect(lambda: self.last_img(False))
        window.pushButton_3.pressed.connect(lambda: self.last_img(False))
        print("init ok")
    def show_pic(self):
        success, frame = self.cap.read()
        if success:
            show = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.window_init()
    window.show()
    sys.exit(app.exec_())
