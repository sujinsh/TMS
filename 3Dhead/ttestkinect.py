import numpy as np
import time
import pyk4a
from pyk4a import Config, PyK4A
import cv2
import threading
from helpers import colorize
import k4a_module
from enum import IntEnum


class CalibrationType(IntEnum):
    UNKNOWN = -1  # Unknown
    DEPTH = 0  # Depth Camera
    COLOR = 1  # Color Sensor
    GYRO = 2  # Gyroscope
    ACCEL = 3  # Accelerometer
    NUM = 4  # Number of types excluding unknown type


class Camera(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.k4a = PyK4A(
            Config(
                color_resolution=pyk4a.ColorResolution.RES_720P,
                camera_fps=pyk4a.FPS.FPS_30,
                depth_mode=pyk4a.DepthMode.WFOV_2X2BINNED,
                synchronized_images_only=True,))

        self.camera_opened = False
        self.color_w = 1280
        self.color_h = 720
        # self.depth_img = None
        # self.ir_img = None
        # self.color_img = None
        # self.tf_color_img = None
        # self.tf_depth_img = None
        # self.tf_ir_img = None
        self.capture = None

    def start_kinect(self):
        if self.camera_opened:
            return
        try:
            self.k4a.start()
            self.camera_opened = True
        except Exception as e:
            print(e)
            print("请检查相机是否开启")
            self.camera_opened = False
        print("start video")

    def stop_kinect(self):
        if not self.camera_opened:
            return
        self.camera_opened = False
        self.k4a.stop()
        print("camera stop")

    def color2point(self, color_img_pix, hflip=False, vflip=False):     # 返回Kinect相加下某个像素点的三维坐标(pix_x, pix_y, depth)
        pix_x, pix_y = color_img_pix[0], color_img_pix[1]
        if hflip:
            pix_x = self.color_w - pix_x
        if vflip:
            pix_y = self.color_h - pix_y

        if self.capture is not None:
            # print(depth)

            depth, num = 0, 0
            for dx in [-2,-1,0,1,2]:        # 像素点深度的均值滤波
                for dy in [-2,-1,0,1,2]:
                    d = self.capture.transformed_depth[pix_y+dy][pix_x+dx]
                    if d != 0:
                        depth += d
                        num += 1
            # print("depth", depth)
            if num == 0:  # depth 0 too far
                return np.array([0.0, 0.0, 0.0])
                # depth = 10000
            else:
                depth /= num
            p = self.k4a.calibration.convert_2d_to_3d((pix_x, pix_y),
                                                         depth, CalibrationType.COLOR, CalibrationType.COLOR)
            p = np.array(p)
            # print("point:", p)
            return p

    def get_img(self, type="color"):
        if not self.camera_opened:
            return None
        if type == "color" or type == "c":
            return self.capture.color
        elif type == "depth" or type == "d":
            return colorize(self.capture.depth, (None, 5000))
        elif type == "ir":
            return colorize(self.capture.ir, (None, 500), colormap=cv2.COLORMAP_JET)
        elif type == "tc" or type == "transformed color":
            return self.capture.transformed_color
        elif type == "td" or type == "transformed depth":
            return colorize(self.capture.transformed_depth, (None, 5000))
        elif type == "tir" or type == "transformed ir":
            return colorize(self.capture.transformed_ir, (None, 500), colormap=cv2.COLORMAP_JET)
        return None

    def run(self):
        self.start_kinect()
        time.sleep(1)
        # 循环接收数据
        while self.camera_opened:
            capture = self.k4a.get_capture()
            self.capture = capture
            # if capture.depth is not None:
            #     self.depth_img = colorize(capture.depth, (None, 5000))
            # if capture.ir is not None:
            #     self.ir_img = colorize(capture.ir, (None, 500), colormap=cv2.COLORMAP_JET)
            # if capture.color is not None:
            #     self.color_img = capture.color
            # if capture.transformed_depth is not None:
            #     self.tf_depth_img = colorize(capture.transformed_depth, (None, 5000))
            # if capture.transformed_color is not None:
            #     self.tf_color_img = capture.transformed_color
            # if capture.transformed_ir is not None:
            #     self.tf_ir_img = colorize(capture.transformed_ir, (None, 500), colormap=cv2.COLORMAP_JET)

            time.sleep(0.02)

cx, cy = 100, 100
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global cx, cy
        cx, cy = x, y
        print(cx, cy)

if __name__ == "__main__":
    import mediapipe as mp
    ca = Camera()
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()  # 设置参数，详见 hands.py 中的 __init__
    mpDraw = mp.solutions.drawing_utils  # 将检测出的手上的标记点连接起来
    ca.start()
    cv2.namedWindow("bimg")
    cv2.setMouseCallback("bimg", on_EVENT_LBUTTONDOWN)
    time.sleep(2)
    while 1:
        img = ca.get_img('td')
        # img = ca.get_img('c')
        # print(ca.capture.transformed_depth)
        if img is not None:
            # height, width, channel = img[:, :, :3].shape
            # img = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2RGB)
            # results = hands.process(img)  # 对输入图像进行处理，探索图像中是否有手
            # if results.multi_hand_landmarks:
            #     for handLms in results.multi_hand_landmarks:  # 捕捉画面中的每一只手
            #         mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)  # 给画面中的每一只手进行标点、连线的操作
            #
            #         # 取0, 5, 13 三个关节计算手坐标系
            #         id = 0
            #         lm = handLms.landmark[id]
            #         # for id, lm in enumerate(handLms.landmark):
            #         h, w, c = img.shape
            #         cx, cy = int(lm.x * w), int(lm.y * h)  # 根据比例还原出每一个标记点的像素坐标
            #         # if not cxmin<=cx<=cxmax:
            #         #     continue
            #         # if not cymin<=cy<=cymax:
            #         #     continue
            #         print(cx, cy)
            #         p0 = ca.color2point([cx, cy])
            #         if p0 is None or not any(p0) or any(np.isnan(p0)) or any(np.isinf(p0)):
            #             continue
            #         print(p0)
            # img = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2RGB)
            # cv2.flip(img, -1)
            # print(ca.color2point([600, 360]))
            img = cv2.flip(img, -1)     # 图片翻转

            info = str([int(i) for i in ca.color2point([cx, cy], vflip=True, hflip=True)])
            cv2.circle(img, (cx, cy), 1, (0, 0, 255), thickness=-1)
            cv2.putText(img, info, (cx, cy), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 0), thickness=1)
            cv2.imshow('bimg', img)
            # img = img[ 70:620,450:830, :]
            # cv2.imshow('aimg', img)
            s = cv2.waitKey(1)
            if s == 27:  # ESC=27
                cv2.destroyAllWindows()
                break
        else:
            time.sleep(0.1)
    ca.stop_kinect()
