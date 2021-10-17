import numpy as np
import time
from primesense import openni2
from primesense import _openni2 as c_api
import cv2
import threading
from helpers import colorize
from enum import IntEnum

flame2mps = [70, 63, 105, 66, 107, 336, 296, 334, 293, 300, 168, 6, 195, 4, 98, 97, 2, 326, 327, 33, 159, 157, 133, 153, 144, 362, 384, 386, 263, 373, 380, 61, 39, 37, 0, 267, 269, 291, 321, 314, 17, 84, 181, 78, 82, 13, 312, 308, 317, 14, 87]

class CalibrationType(IntEnum):
    UNKNOWN = -1  # Unknown
    DEPTH = 0  # Depth Camera
    COLOR = 1  # Color Sensor
    GYRO = 2  # Gyroscope
    ACCEL = 3  # Accelerometer
    NUM = 4  # Number of types excluding unknown type


class Camera(threading.Thread):
    def __init__(self, file_pass):
        threading.Thread.__init__(self)
        openni2.initialize(file_pass)

        self.camera_opened = False
        self.color_frame_data = None
        self.depth_frame_data = None
        self.color_w = 640
        self.color_h = 480
        self.dev = None

    def start_orbbec(self):
        if self.camera_opened:
            return
        try:
            self.dev = openni2.Device.open_any()
            self.depth_stream = self.dev.create_depth_stream()
            self.depth_stream.start()
            self.depth_stream.set_video_mode(
                c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
                                   resolutionX=640, resolutionY=480, fps=30))
            # 图像像素对齐
            if self.dev.is_image_registration_mode_supported(
                    c_api.OniImageRegistrationMode.ONI_IMAGE_REGISTRATION_DEPTH_TO_COLOR):
                self.dev.set_image_registration_mode(c_api.OniImageRegistrationMode.ONI_IMAGE_REGISTRATION_DEPTH_TO_COLOR)

            self.color_stream = self.dev.create_color_stream()
            self.color_stream.start()
            self.color_stream.set_video_mode(
                c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
                                   resolutionX=640, resolutionY=480, fps=30))

            self.camera_opened = True
        except Exception as e:
            print(e)
            print("请检查相机是否开启")
            self.camera_opened = False
        print("start video")

    def stop_orbbec(self):
        if not self.camera_opened:
            return
        self.camera_opened = False
        openni2.unload()
        print("camera stop")

    def color2point(self, color_img_pix, hflip=False, vflip=False):
        pix_x, pix_y = color_img_pix[0], color_img_pix[1]
        if hflip:
            pix_x = self.color_w - pix_x
        if vflip:
            pix_y = self.color_h - pix_y

        if self.dev is not None:
            # print(depth)
            depth, num = 0, 0
            depthData = self.get_img('d')
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    d = depthData[pix_y+dy, pix_x+dx][0]
                    if d != 0:
                        depth += d
                        num += 1
            # print("depth", depth)
            if num == 0:  # depth 0 too far
                return np.array([0.0, 0.0, 0.0])
                # depth = 10000
            else:
                depth /= num
            # depth /=10
            p = openni2.convert_depth_to_world(self.depth_stream, pix_x, pix_y, depth)
            p = np.array(p)
            p[2] /= 10
            # print("point:", p)
            return p

    def color_update(self):
        frame = self.color_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        return frame_data

    def depth_update(self):
        frame = self.depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        return frame_data

    def destructor(self):
        openni2.unload()

    def get_img(self, type="color"):
        if not self.camera_opened:
            return None
        if type == "color" or type == "c" and self.color_frame_data != None:
            img = np.frombuffer(self.color_frame_data, dtype=np.uint8)
            img.shape = (480, 640, 3)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img
        elif type == "depth" or type == "d":
            img = np.frombuffer(self.depth_frame_data, dtype=np.uint16)
            # img.shape = (1, 480, 640)
            img = img.reshape(480, 640, 1)
            # return colorize(img, (None, 5000))
            return img
        # elif type == "ir":
        #     return colorize(self.capture.ir, (None, 500), colormap=cv2.COLORMAP_JET)
        # elif type == "tc" or type == "transformed color":
        #     return self.capture.transformed_color
        # elif type == "td" or type == "transformed depth":
        #     return colorize(self.capture.transformed_depth, (None, 5000))
        # elif type == "tir" or type == "transformed ir":
        #     return colorize(self.capture.transformed_ir, (None, 500), colormap=cv2.COLORMAP_JET)
        return None

    def run(self):
        self.start_orbbec()
        time.sleep(1)
        # 循环接收数据
        while self.camera_opened:
            self.color_frame_data = self.color_update()
            self.depth_frame_data = self.depth_update()
            time.sleep(0.02)


def mousecallback(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        # print(param)
        print("Pix location")
        print(x, y)
        print(param.color2point([x,y]))

# 利用对称性去将无深度的点进行补充，缺点：若两对称点均无深度或者无深度的点为中间点则深度依旧为0
def find_depth_with_symmetry(id, points_51_depth):
    # id 是中间点
    if id in [11, 12, 13, 14, 17, 35, 46, 50, 41]:
        return 0
    if id in range(1, 11):
        if id > 5:
            return points_51_depth[id - 5 - 1]
        else:
            return points_51_depth[id + 5 - 1]
    if id in range(15, 20):
        return points_51_depth[34 - id - 1]
    if id in range(20, 32):
        if id > 25:
            return points_51_depth[id - 6 - 1]
        else:
            return points_51_depth[id + 6 - 1]
    if id in range(32, 39):
        return points_51_depth[70 - id - 1]
    if id in range(39, 44):
        return points_51_depth[82 - id - 1]
    if id in range(44, 49):
        return points_51_depth[92 - id - 1]
    if id in range(49, 52):
        return points_51_depth[100 - id - 1]

# 利用局部性，将无深度点的周围点的深度进行统计，且按照一定的权重，离得越远权重越低，离得近则权重高
def find_depth_with_neighborpoint(id_x, id_y, points_all_depth):
    max_radius = 10
    neighbors_depth = []
    # m是搜索矩阵的行数
    m = min(points_all_depth.shape[0], id_y + max_radius) - max(0, id_y - max_radius) + 1
    # n是搜索矩阵的列数
    n = min(points_all_depth.shape[1], id_x + max_radius) - max(0, id_x - max_radius) + 1
    x, y = max(0, id_x - max_radius), max(0, id_y - max_radius)
    for i in range((min(m, n) + 1) // 2):
        # 从左到右遍历“上边”
        for j in range(i, n - i):
            if points_all_depth[x + i][y + j] != 0:
                # print(points_all_depth[x + i][y + j])
                neighbors_depth.append([points_all_depth[x + i][y + j], max_radius + 1 - max(abs(x + i - id_x), abs(y + j - id_y))]) # 存储格式:[depth_val, radius]，radius是作为该点深度的权值
        # 从上到下遍历“右边”
        for j in range(i + 1, m - i):
            if points_all_depth[x + i][y + j] != 0:
                # print(points_all_depth[x + i][y + j])
                neighbors_depth.append([points_all_depth[x + i][y + j], max_radius + 1 - max(abs(x + i - id_x), abs(y + j - id_y))])
        # 从右到左遍历“下边”
        for j in range(i + 1, n - i):
            if points_all_depth[x + i][y + j] != 0:
                # print(points_all_depth[x + i][y + j])
                neighbors_depth.append([points_all_depth[x + i][y + j], max_radius + 1 - max(abs(x + i - id_x), abs(y + j - id_y))])
        # 从下到上遍历“左边”
        for j in range(i + 1, m - 1 - j):
            if points_all_depth[x + i][y + j] != 0:
                # print(points_all_depth[x + i][y + j])
                neighbors_depth.append([points_all_depth[x + i][y + j], max_radius + 1 - max(abs(x + i - id_x), abs(y + j - id_y))])
    id_depth = 0
    neighbors_depth = np.array(neighbors_depth)
    # print(np.sum(neighbors_depth, axis=0))
    # weight_sum = np.sum(neighbors_depth, axis=0)[1]
    for nb_depth in neighbors_depth:
        # id_depth += nb_depth[0] * nb_depth[1] / weight_sum
        id_depth += nb_depth[0]
    id_depth //= len(neighbors_depth)
    return int(id_depth)


if __name__ == "__main__":
    import mediapipe as mp
    ca = Camera("D:/windows/SDK/x64/Redist")
    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    ca.start()
    time.sleep(2)
    cv2.namedWindow("bimg")
    time.sleep(3)
    while 1:
        img = ca.get_img('c')
        if img is not None:

            depthData = ca.get_img('d')
            cv2.setMouseCallback("bimg", mousecallback, ca)
            scale = 5
            w, h = 640, 480
            image_roi = cv2.resize(img, (w * scale, h * scale))

            with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
                results = face_mesh.process(image_roi)
                if results.multi_face_landmarks is not None:
                    for face_landmarks in results.multi_face_landmarks:
                        points = []
                        for i in range(len(flame2mps)):
                            lm = face_landmarks.landmark[flame2mps[i]]
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            points.append([cx, cy, depthData[cy, cx][0]])
                        np.save('./data/init_lmk.npy', points)

                        points1 = np.array(points)
                        for i in range(len(flame2mps)):
                            if points1[i][2] == 0:
                                points1[i][2] = find_depth_with_symmetry(i + 1, points1[:, 2])
                        np.save('./data/symmetry_lmk.npy', points1)

                        # points2 = np.array(points)
                        # for i in range(len(flame2mps)):
                        #     if points2[i][2] == 0:
                        #         # print(depthData.shape, depthData.shape[0])
                        #         points2[i][2] = find_depth_with_neighborpoint(points2[i][0], points2[i][1], depthData)
                        # np.save('./data/neighbor_lmk.npy', points2)

                        mp_drawing.draw_landmarks(
                            image=img,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACE_CONNECTIONS,
                            landmark_drawing_spec=drawing_spec,
                            connection_drawing_spec=drawing_spec)

            # img = cv2.flip(img, -1)

            # info = str([int(i) for i in ca.color2point([cx, cy], vflip=True, hflip=True)])
            # cv2.circle(img, (cx, cy), 1, (0, 0, 255), thickness=-1)
            # cv2.putText(img, info, (cx, cy), cv2.FONT_HERSHEY_PLAIN,
            #             1.0, (0, 0, 0), thickness=1)
            cv2.imshow('bimg', img)
            cv2.imshow('depth', depthData)
            # img = img[ 70:620,450:830, :]
            # cv2.imshow('aimg', img)
            s = cv2.waitKey(1)
            if s == 27:  # ESC=27
                cv2.destroyAllWindows()
                break
        else:
            time.sleep(0.1)
    ca.destructor()
