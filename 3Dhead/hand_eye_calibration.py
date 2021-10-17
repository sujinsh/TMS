#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
import numpy as np
import time
# from ttestkinect import Camera
import cv2
import threading
from math import pi
import os
from ttestorbbec import Camera

def get_chessbox_point():
    ca = Camera("D:/windows/SDK/x64/Redist")
    ca.start()
    time.sleep(2)

    w, h = 5, 4
    criteria = (cv2.TERM_CRITERIA_EPS +
                cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objpoints = np.ones((h * w, 3), dtype=np.float64)  # point cloud

    while 1:
        img = ca.get_img("c")
        scale = 2
        if img is not None:
            imgh, imgw, imgc = img.shape
            img = cv2.resize(img, (int(imgw*scale), int(imgh*scale)))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (w, h), None)
            if ret == True:
                cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

                cv2.drawChessboardCorners(img, (w, h), corners, ret)
                # cv2.imshow('findCorners', img)
                simg = cv2.resize(img, (imgw, imgh))
                cv2.imshow("img", simg)
                s = cv2.waitKey(5)
                if s == 27:  #ESC
                    for i in range(w * h):
                        cor = corners[i][0]
                        pixel_point = [int(cor[0]/scale), int(cor[1]/scale)]

                        # pixel_point = [int(cor[0]/3), int(cor[1]/3)]
                        print(pixel_point)
                        objpoints[i, :] = np.array(ca.color2point(pixel_point)).reshape(1, 3)
                    # show corners
                    print(objpoints)
                    print("accuracy:")
                    for i in range(0, h):
                        for j in range(1, w):
                            print(np.linalg.norm(objpoints[i * w + j, :] - objpoints[i * w + j - 1, :]))
                    for i in range(1, h):
                        for j in range(0, w):
                            print(np.linalg.norm(objpoints[i * w + j, :] - objpoints[(i - 1) * w + j, :]))

                    np.save('camera_corners_point.npy', objpoints)
                    print("OK")
                    break

            else:
                print("corners not found")

        else:
            time.sleep(0.2)

    # cv2.destroyAllWindows()

def generate_robot_points():
    # config of the chessbox
    w, h, L = 5, 4, 34
    # change the follow 3 lines
    # the very first point of corners (red)
    x1, y1, z1 = 413.353, 55.122, -140.544

    # the end point of the first line (red)
    x2, y2, z2 = 414.664, -80.823, -136.767
    # the last point of the corners
    x3, y3, z3 = 474.869, -82.699, -219.358
    robot_points = np.ones((h*w, 3), dtype=np.float64)
    VW = np.array([x2-x1, y2-y1, z2-z1], dtype=np.float64) / (w-1)
    VH = np.array([x3-x2, y3-y2, z3-z2], dtype=np.float64) / (h-1)
    print("accuracy:")
    print("l error(mm):", abs(np.linalg.norm(VW) - L))
    print("h error(mm)", abs(np.linalg.norm(VH) - L))
    if abs(np.linalg.norm(VW) - L) > 1.2 or abs(np.linalg.norm(VH) - L) > 1.2:
        print("NG")
        return -1

    p0 = np.array([x1, y1, z1])
    for i in range(h):
        for j in range(w):
            robot_points[i*w+j, :] = p0 + i * VH + j*VW

    np.save("robot_corners_points", robot_points)
    print("robot_points:", robot_points)
    print("OK")
    return 0

def cali_rotation_translation():
    world_points = np.load('robot_corners_points.npy')
    camery_points = np.load('camera_corners_point.npy')

    world_center = np.mean(world_points, axis=0)
    camery_center = np.mean(camery_points, axis=0)

    q2 = world_points - world_center.reshape(1, 3)
    q1 = camery_points - camery_center.reshape(1, 3)

    W = np.dot(q1.T, q2)
    U, S, Vt = np.linalg.svd(W)
    R = np.dot(Vt.T, U.T)
    if np.linalg.det(R) < 0:
        print("det R is < 0")
        Vt[2, :] *= -1
        R = np.dot(Vt.T, U.T)

    t = np.dot(-R, camery_center.reshape(3, 1)) + world_center.reshape(3, 1)
    print("R = ", R)
    print("t = ", t)
    word_ = np.dot(R, camery_points.T)+t.reshape(3, 1)
    print("accuracy:")
    print(word_.T - world_points)

    return R, t


if __name__ == "__main__":

    print("-----------------------------------------------------------------------")
    # :::::::::::::::::::::::::::calibration :::::::::::::::::::::::::::::::
    # step 1.-------get camera chessbox corners points----------------------
    # get_chessbox_point()
    #
    # step 2.--------get robot chessbox corners points----------------------
    # generate_robot_points()

    # step 3.--------calculate the rotation and translation matrix----------
    cali_rotation_translation()
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # camery_points = np.load('camera_corners_point.npy')
    # world_points = np.load('robot_corners_points.npy')
    # # #
    # print(camery_points)
    # print(world_points)
    # R = np.array([[0.1215947, 0.13433768, -0.98344706],
    #               [-0.99242063, 0.03419943, -0.1180326],
    #               [0.0177771, 0.99034529, 0.13747796]])
    # t = np.array([[1641.55634999],
    #                    [125.54391666],
    #                    [-173.11738404]])
    # print(np.dot(R, camery_points[0]) + t.reshape(1,3))

    # cv2.destroyAllWindows()
