#!/usr/bin/env python3
'''
from datetime import datetime
import time
import argparse
import sys
import configparser
import os
from openni import openni2
from openni import _openni2 as c_api
import cv2
import numpy as np



def parse_args():
    # PARAMETERS
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=640, help='resolutionX')
    parser.add_argument('--height', type=int, default=400, help='resolutionY')
    parser.add_argument('--fps', type=int, default=30, help='frame per second')
    parser.add_argument('--mirroring', default=True, help='mirroring [default: False]')
    parser.add_argument('--compression', default=True, help='compress or not, when saving the video [default: True]')

    return parser.parse_args()


def getOrbbec():
    # 记载 openni
    try:
        if sys.platform == "win32":
            libpath = r"D:\windows\SDK\x64\Redist"
        else:
            libpath = "lib/Linux"
        print("library path is: ", libpath)
        # openni2.initialize(os.path.join(os.path.dirname(__file__), libpath))
        openni2.initialize(libpath)
        print("OpenNI2 initialized \n")
    except Exception as ex:
        print("ERROR OpenNI2 not initialized", ex, " check library path..\n")
        return

    # 加载 orbbec 相机
    try:
        device = openni2.Device.open_any()
        return device
    except Exception as ex:
        print("ERROR Unable to open the device: ", ex, " device disconnected? \n")
        return


def main(args):
    device = getOrbbec()
    # 创建深度流
    depth_stream = device.create_depth_stream()
    depth_stream.set_mirroring_enabled(args.mirroring)
    # depth_stream.set_video_mode(c_api.OniVideoMode(resolutionX=args.width, resolutionY=args.height, fps=args.fps,
    #                                                pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM))

    depth_video_mode = openni2.VideoMode()
    depth_video_mode.fps = args.fps
    depth_video_mode.pixelFormat = openni2.PIXEL_FORMAT_DEPTH_1_MM
    depth_video_mode.resolutionX = args.width
    depth_video_mode.resolutionY = args.height
    depth_stream.set_video_mode(depth_video_mode)


    # 获取uvc
    cap = cv2.VideoCapture(0)

    # 设置 镜像 帧同步
    device.set_image_registration_mode(True)
    device.set_depth_color_sync_enabled(True)
    depth_stream.start()

    while True:
        # 读取帧
        frame_depth = depth_stream.read_frame()
        frame_depth_data = frame_depth.get_buffer_as_uint16()
        # 读取帧的深度信息 depth_array 也是可以用在后端处理的 numpy格式的
        depth_array = np.ndarray((frame_depth.height, frame_depth.width), dtype=np.uint16, buffer=frame_depth_data)
        # 变换格式用于 opencv 显示
        depth_uint8 = 1 - 250 / (depth_array )
        depth_uint8[depth_uint8 > 1] = 1
        depth_uint8[depth_uint8 < 0] = 0
        cv2.imshow('depth', depth_uint8)

        # 读取 彩色图
        _, color_array = cap.read()
        cv2.imshow('color', color_array)

        # 对彩色图 color_array 做处理

        # 对深度图 depth_array 做处理

        # 键盘监听
        if cv2.waitKey(1) == ord('q'):
            # 关闭窗口 和 相机
            depth_stream.stop()
            cap.release()
            cv2.destroyAllWindows()
            break

    # 检测设备是否关闭（没什么用）
    try:
        openni2.unload()
        print("Device unloaded \n")
    except Exception as ex:
        print("Device not unloaded: ", ex, "\n")


if __name__ == '__main__':
    args = parse_args()
    main(args)
'''


'''
import numpy as np
from openni import openni2
from openni import _openni2
import cv2 as cv
import open3d
import copy
import time


SAVE_POINTCLOUDS = False


def get_rgbd(color_capture, depth_stream, depth_scale=1000, depth_trunc=4, convert_rgb_to_intensity=False):

    # Get color image
    _, color_image = color_capture.read()
    color_image = color_image[:, ::-1, ::-1]

    # Get depth image
    depth_frame = depth_stream.read_frame()
    depth_image = np.frombuffer(depth_frame.get_buffer_as_uint16(), np.uint16)
    depth_image = depth_image.reshape(depth_frame.height, depth_frame.width)
    depth_image = depth_image.astype(np.float32)

    # Create rgbd image from depth and color
    color_image = np.ascontiguousarray(color_image)
    depth_image = np.ascontiguousarray(depth_image)
    rgbd = open3d.geometry.RGBDImage.create_from_color_and_depth(
        open3d.geometry.Image(color_image),
        open3d.geometry.Image(depth_image),
        depth_scale=depth_scale,
        depth_trunc=depth_trunc,
        convert_rgb_to_intensity=convert_rgb_to_intensity
    )

    return rgbd


def main():
    # Init openni
    openni_dir = "D:/windows/SDK/x64/Redist"
    openni2.initialize(openni_dir)

    # Open astra color stream (using opencv)
    color_capture = cv.VideoCapture(2)
    color_capture.set(cv.CAP_PROP_FPS, 5)
    print(color_capture.read())

    # Open astra depth stream (using openni)
    depth_device = openni2.Device.open_any()
    depth_stream = depth_device.create_depth_stream()
    depth_stream.start()
    depth_stream.set_video_mode(
        _openni2.OniVideoMode(pixelFormat=_openni2.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM,
                              resolutionX=640,
                              resolutionY=480,
                              fps=5))
    depth_device.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)

    # Create pointcloud visualizer
    visualizer = open3d.visualization.Visualizer()
    visualizer.create_window("Pointcloud", width=1000, height=700)

    # Camera intrinsics of the astra pro
    astra_camera_intrinsics = open3d.camera.PinholeCameraIntrinsic(
        width=640,
        height=480,
        fx=585,
        fy=585,
        cx=320,
        cy=250)

    # Create initial pointcloud
    pointcloud = open3d.geometry.PointCloud()
    visualizer.add_geometry(pointcloud)

    first = True
    prev_timestamp = 0
    num_stored = 0

    while True:
        rgbd = get_rgbd(color_capture, depth_stream)

        # Convert images to pointcloud
        new_pointcloud = open3d.geometry.PointCloud.create_from_rgbd_image(
            rgbd,
            intrinsic=astra_camera_intrinsics,
        )
        # Flip pointcloud
        new_pointcloud.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
        # Set rendered pointcloud to recorded pointcloud
        pointcloud.points = new_pointcloud.points
        pointcloud.colors = new_pointcloud.colors

        # Save pointcloud each n seconds
        if SAVE_POINTCLOUDS and time.time() > prev_timestamp + 5:
            filename = "pointcloud-%r.pcd" % num_stored
            open3d.io.write_point_cloud(filename, new_pointcloud)
            num_stored += 1
            print("Stored: %s" % filename)
            prev_timestamp = time.time()

        # Reset viewpoint in first frame to look at the scene correctly
        # (e.g. correct bounding box, direction, distance, etc.)
        if first:
            visualizer.reset_view_point(True)
            first = False

        # Update visualizer
        visualizer.update_geometry()
        visualizer.poll_events()
        visualizer.update_renderer()


if __name__ == "__main__":
    main()
'''

import cv2
import numpy as np
from primesense import openni2
from primesense import _openni2 as c_api




'''
class OpenniClass:
    def __init__(self, file_pass):
        openni2.initialize(file_pass)
        dev = openni2.Device.open_any()
        self.color_stream = dev.create_color_stream()
        self.color_stream.start()
        self.color_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
                               resolutionX=640, resolutionY=480, fps=30))

        self.depth_stream = dev.create_depth_stream()
        self.depth_stream.start()
        self.depth_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
                               resolutionX=640, resolutionY=480, fps=30))

        # self.ir_stream = dev.create_ir_stream()
        # self.ir_stream.start()
        # self.depth_stream.set_video_mode(
        #     c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_GRAY16,
        #                        resolutionX=640, resolutionY=480, fps=30))

    def color_update(self):
        frame = self.color_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint8)
        img.shape = (480, 640, 3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def ir_update(self):
        frame = self.ir_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img2 = np.frombuffer(frame_data, dtype=np.uint16)
        return img2

    def depth_update(self):
        frame = self.depth_stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()
        img = np.frombuffer(frame_data, dtype=np.uint16)
        # img.shape = (1, 480, 640)
        img1 = img.reshape(480, 640, 1)
        return img1

    def depth_update_(self, min, max):
        img = self.depth_update()
        float_ = np.zeros(img.shape[:2], dtype=np.float64)
        out = np.zeros(img.shape[:2], dtype=np.uint8)
        img[img < min] = min
        img[img > max] = min
        float_ = img.astype(np.float64)
        float_ = float_ - min
        float_ = ((max - min) - float_) / (max - min) * 255.0
        out = float_.astype(np.uint8)
        return out

    def destructor(self):
        openni2.unload()

astra = OpenniClass("D:/windows/SDK/x64/Redist")

while True:
    colorImg = astra.color_update()
    depthImg = astra.depth_update_(4000, 8000)
    # irImg = astra.ir_update()
    #raw_data
    depthData = astra.depth_update()

    cv2.imshow("color", colorImg)
    cv2.imshow("depth", depthImg)
    # cv2.imshow('IR', irImg)

    xyz = []

    def mousecallback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # xyz.append(x)
            # xyz.append(y)
            # xyz.append(param[y, x][0])
            print(x, y, param[y, x][0])
            print('world xyz: ', openni2.convert_depth_to_world(astra.depth_stream, x, y, param[y, x][0]))
            # print(type(openni2.convert_depth_to_world(astra.depth_stream, xyz[0], xyz[1], xyz[2])))

    cv2.setMouseCallback('color', mousecallback, depthData)
    if xyz != []:
        print('xyz: ', xyz)
        print('world xyz: ', openni2.convert_depth_to_world(astra.depth_stream, xyz[0], xyz[1], xyz[2]))
        xyz.clear()


    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

astra.destructor()
'''




def color_update():
    frame = color_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    img = np.frombuffer(frame_data, dtype=np.uint8)
    img.shape = (480, 640, 3)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def depth_update():
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    img = np.frombuffer(frame_data, dtype=np.uint16)
    img.shape = (1, 480, 640)
    img1 = img.reshape(480, 640, 1)
    return img1

openni_dir = "D:/windows/SDK/x64/Redist"
openni2.initialize(openni_dir)
dev = openni2.Device.open_any()


depth_stream = dev.create_depth_stream()
depth_stream.start()
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
                       resolutionX=640, resolutionY=480, fps=30))

if dev.is_image_registration_mode_supported(c_api.OniImageRegistrationMode.ONI_IMAGE_REGISTRATION_DEPTH_TO_COLOR):
    dev.set_image_registration_mode(c_api.OniImageRegistrationMode.ONI_IMAGE_REGISTRATION_DEPTH_TO_COLOR)

color_stream = dev.create_color_stream()
color_stream.start()
color_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
                       resolutionX=640, resolutionY=480, fps=30))


def depth_zero_index(depth_data):
    X_Y = np.where(depth_data == 0)
    X = X_Y[0]
    Y = X_Y[1]
    return np.vstack((X, Y)).T

while True:
    img = color_update()
    img1 = depth_update()
    ids = depth_zero_index(img1)
    for id in ids:
        img[id[0]][id[1]] = [0, 0, 0]
    cv2.imshow('image', img)
    cv2.imshow('depth', img1)


    def mousecallback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, y, param[y, x][0])


    cv2.setMouseCallback('image', mousecallback, img1)


    cv2.waitKey(1)
cv2.destroyAllWindows()
