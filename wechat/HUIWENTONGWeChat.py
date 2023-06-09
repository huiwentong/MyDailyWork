import multiprocessing
import os.path
import sys

import win32print
from wxauto import *
import time
import datetime
import random
import win32gui
from wechatAuto_ui import Ui_MainWindow
from pynput.mouse import Button, Controller as mC
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtWidgets, QtCore, QtGui
import traceback
from multiprocessing import Process, Manager
import ctypes
from qt_material import apply_stylesheet
# 获取当前微信客户端
wx = WeChat()


# 获取会话列表
# wx.GetSessionList()
# wx.GetLastMessage()
###############################
# 1、获取默认窗口聊天信息
###############################
# def get_default_window_messages():
#     # 默认是微信窗口当前选中的窗口
#     # 输出当前聊天窗口聊天消息
#     msgs = wx.GetAllMessage
#     for msg in msgs:
#         print('%s : %s' % (msg[0], msg[1]))
#
#     # 获取更多聊天记录
#     wx.LoadMoreMessage()
#     msgs = wx.GetAllMessage
#     for msg in msgs:
#         print('%s : %s' % (msg[0], msg[1]))


def loop(me, target, zaoanTime, gongzuoshijian_start, gongzuoshijian_end, xiabanshijian_start, a, imwork, night, log,
         on, setfore):
    while True:

        try:
            if not on.value:
                return
            time.sleep(2)
            setfore.value = False
            mouse = mC()
            currentp = mouse.position
            date = str(datetime.datetime.now())
            # print(date[11:16])
            if date[11:16] == zaoanTime.value:
                wx.ChatWith(target.value)
                print(target.value)
                time.sleep(5)
                test = wx.GetLastMessage
                time.sleep(2)
                if test[0] == me.value and test[1].endswith('[爱心][爱心][爱心][嘴唇][嘴唇][嘴唇]'):
                    print(me.value)
                    continue
                else:
                    ran = random.randint(0, len(a) - 1)
                    zaoan = '[太阳]' + a[ran] + '……早安我的甜！' + '[爱心][爱心][爱心][嘴唇][嘴唇][嘴唇]'
                    wx.SendMsg(zaoan)
                setfore.value = True
                # mouse.position = currentp
            if int(date[11:13]) > gongzuoshijian_start.value and int(date[11:13]) < gongzuoshijian_end.value:
                if int(date[14:16]) == 50:
                    print(date[14:16])
                    log.value += str(date[14:16]) + '\n'
                    wx.ChatWith(target.value)
                    time.sleep(5)
                    last = wx.GetAllMessage
                    print(last)
                    log.value += str(last) + '\n'
                    time.sleep(2)
                    if last[-1][0] == target.value and last[-1][1] == '[动画表情]' and last[-2][0] == target.value:
                        wx.SendMsg('[爱心][爱心][爱心]')
                    elif last[-1][0] == target.value and last[-1][1] != '[动画表情]' and last[-2][0] == target.value:
                        ranw = random.randint(0, len(imwork) - 1)
                        wx.SendMsg(imwork[ranw])
                setfore.value = True
                # mouse.position = currentp
            if int(date[11:13]) > xiabanshijian_start.value:
                if int(date[14:16]) == 50:
                    wx.ChatWith(target.value)
                    time.sleep(5)
                    list = wx.GetAllMessage
                    if list[-1][0] == target.value:
                        for i in list[-3:]:
                            if i[0] == 'Time':
                                rann = random.randint(0, len(night) - 1)
                                wx.SendMsg(imwork[rann])
                                break
                setfore.value = True
                # mouse.position = currentp
            print(date)
            log.value += str(date) + '\n'
        except:
            log.value += traceback.format_exc()
            print(traceback.format_exc())


class Mainw(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Mainw, self).__init__()
        self.setupUi(self)
        self.setFixedSize(QtCore.QSize(400, 620))
        self.setWindowTitle('自动微信吼吼吼')
        self.label_status = QtWidgets.QTextBrowser()
        self.label_status.setText(log.value)
        self.label_status.setMinimumWidth(380)
        self.label_status.setMaximumHeight(50)
        self.statusbar.addWidget(self.label_status)

        self.checkBox_zaoan_content.setChecked(True)
        self.checkBox__xiaban_content.setChecked(True)
        self.checkBox_gongzuo_content.setChecked(True)

        self.pushButton_main_start.clicked.connect(self.mainclick)
        self.textEdit_myname.textChanged.connect(self.myname)
        self.textEdit_Tarname.textChanged.connect(self.Tarname)
        self.textEdit_zaoan.textChanged.connect(self.zaoan)
        self.spinBox_gongzuoshijian_start.valueChanged.connect(self.gongzuoshijian_S)
        self.spinBox_gongzuoshijian_end.valueChanged.connect(self.gongzuoshijian_E)
        self.spinBox_xiabanshijian_start.valueChanged.connect(self.xiabanshijian_S)
        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.refresh_status)

    def myname(self):
        global me
        me.value = self.textEdit_myname.document().toPlainText()

    def Tarname(self):
        global target
        target.value = self.textEdit_Tarname.document().toPlainText()

    def zaoan(self):
        global zaoanTime
        zaoanTime.value = self.textEdit_zaoan.document().toPlainText()

    def gongzuoshijian_S(self, value):
        global gongzuoshijian_start
        gongzuoshijian_start.value = value

    def gongzuoshijian_E(self, value):
        global gongzuoshijian_end
        gongzuoshijian_end.value = value

    def xiabanshijian_S(self, value):
        global xiabanshijian_start
        xiabanshijian_start.value = value

    def closeEvent(self, event):
        if on.value:
            QtWidgets.QMessageBox().warning(self, '程序还在运行!', '先终止运行再关闭程序')
            event.ignore()
        else:
            event.accept()

    def refresh_status(self):
        global log, handle1
        # print('timeout')
        self.label_status.setText(log.value)
        self.label_status.moveCursor(QtGui.QTextCursor.End)
        self.timer.start(200)
        if setfore.value:
            print(win32gui.GetWindowText(handle1))
            win32gui.BringWindowToTop(handle1)

    def mainclick(self):
        global on, a, test, gongzuoshijian_end, gongzuoshijian_start, xiabanshijian_start, imwork, night, me, target, log, zaoanTime, handle1
        # self.statusbar.showMessage('statusbar is here', 2000)
        if self.checkBox_zaoan_content.isChecked():
            for i in self.plainTextEdit_zaoan_content.document().toPlainText().split(','):
                a.append(i)
        else:
            a = self.plainTextEdit_zaoan_content.document().toPlainText().split(',')

        if self.checkBox_gongzuo_content.isChecked():
            for i in self.plainTextEdit_gongzuo_content.document().toPlainText().split(','):
                imwork.append(i)
        else:
            imwork = self.plainTextEdit_gongzuo_content.document().toPlainText().split(',')

        if self.checkBox__xiaban_content.isChecked():
            for i in self.plainTextEdit_xiaban_content.document().toPlainText().split(','):
                night.append(i)
        else:
            night = self.plainTextEdit_xiaban_content.document().toPlainText().split(',')

        if on.value:
            on.value = False
            self.timer.stop()
            self.pushButton_main_start.setText('点击开始循环')
        else:
            on.value = True
            thread1 = Process(target=loop, args=(
                me, target, zaoanTime, gongzuoshijian_start, gongzuoshijian_end, xiabanshijian_start, a, imwork, night,
                log,
                on, setfore,))
            thread1.start()
            self.timer.start(200)
            self.pushButton_main_start.setText('点击终止循环')


if __name__ == '__main__':
    multiprocessing.freeze_support()
    target = Manager().Value(ctypes.c_char_p, 'Tiantian')
    me = Manager().Value(ctypes.c_char_p, '派拉萌')
    zaoanTime = Manager().Value(ctypes.c_char_p, '09:00')
    gongzuoshijian_start = Manager().Value('i', 9)
    gongzuoshijian_end = Manager().Value('i', 20)
    xiabanshijian_start = Manager().Value('i', 20)
    a = Manager().list([
        '世上不爱的理由有很多：忙累为你好性格不合距离远了没有感觉了等等，而爱的表现只有一个：就想和你在一起',
        '我一直想要，和你一起，走上那条美丽的小路。有柔风，有白云，有你在我身旁，倾听我快乐和感激的心',
        '上帝给了你智慧，磨难也如影随形。只有在磨难中，智慧才能够熠熠生辉。不经过战斗的舍弃是懦弱的，不经过磨难的历练是愚蠢的',
        '人生的路，每个阶段一个故事，你无法倒带，也无法跳过去，你需要做的，就是努力的走下去',
        '生活总嘲笑我们太年轻，可青春却不经易老去',
        '一个人的梦想，唯有在另一个人加入时，才有了幸福的重量',
        '不要轻易用过去来衡量生活的幸与不幸！每个人的生命都是可以绽放美丽的，只要你珍惜，善待自己，厚待生活',
        '所有相遇都是三生石上的旧梦前缘',
        '这世界有太多的声音。城市在说，现实在说，过往的人在说。你可以聆听，却不能被淹没',
        '每段爱情在走向终结时，倒带回去，一路上或花草鲜美，或落英缤纷，而最初总是倾心的',
        '把每个睡醒后的早晨当成一件礼物，把每个开心后的微笑当成一个习惯，甜甜，愿你微笑今天，快乐永远!',
        '旅行的好处，不是能见到多少人，见过多美的风景，而是走着走着，在一个际遇下，突然重新认识了自己',
        '清晨到，对着镜子照，照一照，笑一笑，所有烦恼都跑掉，抑郁忧愁全都消，快乐自然不会少。问候跟着来报到，给你道声早，祝你心情妙，一天幸福乐逍遥',
        '真诚的祝愿带给远方的你，愿你事事顺心，快乐相随在我心灵的百花园里，采集金色的鲜花，我把最鲜艳的一朵给你，作为我对你的问候。',
        '减压其实简单，只要早起打个滚；唱个歌；看一场电影；和闺蜜吐个槽；逛个街；回家洗个热水澡，然后一觉睡到天亮。第二天又是一个精力旺盛的自己。',
        '人生就有许多这样的奇迹，看似比登天还难的事，有时轻而易举就可以做到，其中的差别就在于非凡的信念',
        '无论你今天要面对什么，既然走到了这一步，就坚持下去，给自己一些肯定，你比自己想象中要坚强',
        '做一个平静的人，做一个善良的人，做一个微笑挂在嘴边，快乐放在心上的人。愿我小小的问候带给你快乐',
        '我握住一把清晨的阳光，轻轻放在你的床上，愿你从睡梦中醒来时，心中充满了早晨的宁静与安详，那是我为你送上的早安',
        '热乎乎的语言，情绵绵的诗篇，甜蜜蜜的旋律，乐淘淘的笑脸，生活总是在幸福中开始',
        '情若朝阳，徐徐升起，温暖心田;谊若美酒，芳香醇厚，沁人心脾',
        '清晨的微风、飘过窗台抚过发鬓一角，清晨的鸟叫、进入耳朵清醒了笑，大地的环境自然美好',
        '阴天，晴天，总是新的一天;好梦，噩梦，活在当下不是梦;从晚上，到早上，这一刻，你我都在路上',
        '学会承受痛苦，有些话，适合烂在心里。学会选择忘记，有些伤，适合埋在记忆里。当一切坎坷都成为经历，才能够挑战任何风雨',
        '每天都要打扮得能怎么漂亮就怎么漂亮才出门，因为你永远不知道今天会遇见谁;漂亮如果有秘诀，那就是：狠狠宠爱自己',
        '睁开迷人的双眼，看白云片片;舒展美丽的笑脸，听流水潺潺;拥抱快乐的今天，盼好运连连',
        '时钟敲响，骄阳升起，凉风吹荡。在这一天最惬意的时候，赶紧起来，看看这一片蔚蓝的天空吧，它给了我们无尽的希望',
        '你要做一个不动声色的大人了。不准情绪化，不准偷偷想念，不准回头看。去过自己另外的生活。你要听话，不是所有的鱼都会生活在同一片海里',
        '沐浴着清晨那唯美而又柔和的朝阳，开始新的一天。给一点心灵阳光，心灵就会灿烂',
        '看着天边的红日蹦出来一次又一次，希望你的一天也如刚升起的红日一般',
        '人生短短几十年，不要给自己留下了什么遗憾，想笑就笑，想哭就哭，该爱的时候就去爱，无需压抑自己，新的一天总有新的活法',
        '你问我：如果你爱我只有我爱你的十分之一，我还愿不愿意和你在一起？让我告诉你：我愿意，我会努力把另九分给你补齐',
        '美好的一天开始啦！清晨的美好就如青草般芳香，如河溪般清澈，如玻璃般透明，如甘露般香甜',
        '努力是人生的一种精神状态，往往最美的不是的那一刻，而是那段努力奋斗的过程',
        '忘记，尘世的繁琐，清空心底的欲望，每天给自己一个微笑，如此美好，又是新的一天',
        '每一个清晨都值得珍惜，每一个日出，都值得记忆，带着对新一天的期待，看待这个世界，感受生命的阳光！'
    ])
    handle1 = win32gui.FindWindow('SunAwtFrame', None)
    imwork = Manager().list([
        '有点忙，等一会呦[调皮][调皮][调皮]',
        '有点忙，等我回去哈[调皮][调皮][调皮]',
        '等我回去的[调皮][调皮][调皮]',
        '回去说[调皮][调皮][调皮]',
        '事情太多啦，稍等我一下下[裂开][裂开][裂开]',
        '我才看见[捂脸][捂脸][捂脸]，等会哈',
        '忙疯了[捂脸][捂脸][捂脸]，你先去玩会哈',
        '我刚刚看见[捂脸][捂脸][捂脸]',
        '我才看见[捂脸][捂脸][捂脸]',
        '忙着没看手机[捂脸][捂脸][捂脸]',
        '才看手机[捂脸][捂脸][捂脸]',
        '[裂开][裂开][裂开]稍等',
        '真的裂开了[裂开][裂开][裂开]一等',
        '我都没听见手机[捂脸][捂脸][捂脸]',
        '等我忙完[捂脸][捂脸][捂脸]',
        '稍等，一会说哈[捂脸][捂脸][捂脸]',
    ])
    night = Manager().list([
        '才看见[捂脸][捂脸][捂脸]电话会，等我完事的哈',
        '刚刚骑车呢，晚会说哈',
        '刚到家[捂脸][捂脸][捂脸]，稍等我还有点工作',
        '跟我爸说话呢',
        '稍等一下，跟我爸说话呢',
        '累死了，我收拾一下',
        '太忙啦，等会哈',
        '你先玩会，我还得收拾收拾',
        '等会说哈'
        '等会的哈[爱心]'
    ])
    on = Manager().Value(ctypes.c_bool, False)
    test = Manager().Value(ctypes.c_char_p, 'qwewqe\n')
    log = Manager().Value(ctypes.c_char_p, 'start~~~~~~~~~~~~~~~~~~~~~~~~~' + '\n')
    setfore = Manager().Value(ctypes.c_bool, 0)
    app = QApplication(sys.argv)
    w = Mainw()
    w.show()
    sys.exit(app.exec_())
