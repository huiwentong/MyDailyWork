import cv2
from cv2 import cv2 as cv
import numpy as np

if __name__ == "__main__":

    cap = cv.VideoCapture('V_TEST3.mp4')

    img = cv.imread('color.jpg')
    cap.set(cv.CAP_PROP_POS_FRAMES, 100)
    # cap.get(cv.CAP_PROP_POS_FRAMES)
    ret, v = cap.read()
    hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV)


    upper = np.array([99, 255, 255])
    lower = np.array([78, 43, 46])

    masks = cv.inRange(hsv, lower, upper)

    # roi = cv.bitwise_and(img, mask, mask=None)
    # roi = cv.add(img, masks)
    # 图片反相
    roi = cv.bitwise_not(img)
    print('roi.shape[0] is %d and shape[1] is %d' % (roi.shape[0], roi.shape[1]))

    # cv.namedWindow('test_hui', cv.WINDOW_NORMAL)
    # cv.resizeWindow('test_hui', int(roi.shape[1]/2), int(roi.shape[0]/2))
    # cv.imshow('test_hui', roi)


    black = np.zeros((512, 512, 3), np.uint8)

    # 添加文字
    cv.putText(img, r'helllllllo! my tiny world', (100, 500), cv2.FONT_ITALIC, 1, (255, 255, 255), 3, cv.LINE_AA)
    # 画一个矩形
    cv.rectangle(img, (50, 50), (600, 600), (255, 255, 255), 5, cv.LINE_AA)
    print(img.item(50, 50, 0))
    for i in dir(cv):
        if 'PROP' in i:
            print(i)

    cv.namedWindow('my', cv.WINDOW_NORMAL)
    cv.resizeWindow('my', int(img.shape[1]/2), int(img.shape[0]/2))
    cv.imshow('my', v)

    cvt = cv.cvtColor(v, cv.COLOR_BGR2RGB)
    # numpy的切片功能
    cvt[int(cvt.shape[0]/2):, int(cvt.shape[1]/2):] = cvt[0: int(cvt.shape[0]/2), 0: int(cvt.shape[1]/2)]
    # 重定义窗口尺寸之前首先要命名窗口
    cv.namedWindow('cvt', cv.WINDOW_NORMAL)
    # 重定义窗口尺寸
    cv.resizeWindow('cvt', int(v.shape[1] / 2), int(v.shape[0] / 2))
    # 图像扩边
    cvt = cv.copyMakeBorder(cvt, 50, 50, 50, 50, cv.BORDER_CONSTANT, (10, 10, 10))
    cv.imshow('cvt', cvt)
    print(cv.waitKey(0) == ord('q'))

    cv.destroyAllWindows()
    cap.release()


