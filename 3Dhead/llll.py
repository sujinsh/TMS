import cv2
from helpers import colorize
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d  # noqa: F401
import mediapipe as mp
import warnings
import math

import pyk4a
from pyk4a import Config, PyK4A

# face_point = [234, 127, 162, 21, 54, 103, 67, 109, 10, 338, 297, 332, 284, 251, 389, 93, 132, 58, 138, 172, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 397, 288, 361, 323, 454, 356]
face_point = [234, 127, 162, 21, 54, 103, 67, 109, 10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93]
left_eye_point = [7, 33, 246, 160, 161, 159, 158, 157, 133, 155, 173, 154, 153, 145, 144, 163]
right_eye_point = [362, 382, 398, 384, 385, 386, 387, 263, 388, 466, 249, 390, 373, 374, 380, 381]


def mean_point(point_list, id_list):
    x, y = 0, 0
    for i in id_list:
        x += point_list[i][0]
        y += point_list[i][1]
    return [x / len(id_list), y / len(id_list)]


def is_fullface(point_list, leye_id_list, reye_id_list, threshold=0.01):
    left_eye_mean_point = mean_point(point_list, leye_id_list)
    right_eye_mean_point = mean_point(point_list, reye_id_list)
    nose_point_x = point_list[4].x
    res = abs(nose_point_x - (left_eye_mean_point[0] + right_eye_mean_point[0]) / 2)
    # print('nose_point_x:', nose_point_x, 'left_eye_mean_point:', left_eye_mean_point, "right_eye_mean_point:", right_eye_mean_point)
    # print(res)
    return res <= threshold

#
# def cal_headcube(capture, point_list):
#     image = capture[:, :, :3]
#     h, w, c = image.shape
#     nose_point = point_list[4]
#     left_face_point = point_list[93]
#     right_face_point = point_list[323]
#     nose_bottom_point = point_list[10]
#     eyebrow_tip_point = point_list[55]  # or 285
#     standard_vec = capture[int(nose_point.x * w)][int(nose_point.y * h)][:2] \
#                    - capture[int(left_face_point.x * w)][int(left_face_point.y * h)][:2]
#     # a = int(standard_vec[0] * 0.04 / (nose_point.x - left_face_point.x))  # ear: (5*128)长度
#     # b = int(standard_vec[1] * 0.19 / (nose_point.y - left_face_point.y))  # 发际线到头顶长度
#     a = int(w * 0.04)
#     b = int(h * 0.19)
#     D1 = abs(capture[int(nose_point.x * w)][int(nose_point.y * h)][2]
#              - capture[int(left_face_point.x * w)][int(left_face_point.y * h)][2])
#     D2 = abs(capture[int(nose_point.x * w)][int(nose_point.y * h)][2]
#              - capture[int(right_face_point.x * w)][int(right_face_point.y * h)][2])
#     D = 2 * max(D1, D2)
#     W1 = abs(capture[int(nose_point.x * w)][int(nose_point.y * h)][0]
#              - capture[int(left_face_point.x * w)][int(left_face_point.y * h)][0])
#     W2 = abs(capture[int(nose_point.x * w)][int(nose_point.y * h)][0]
#              - capture[int(right_face_point.x * w)][int(right_face_point.y * h)][0])
#     W = 2 * (max(W1, W2) + a)
#     H = 3 * abs(capture[int(nose_bottom_point.x * w)][int(nose_bottom_point.y * h)][1]
#                 - capture[int(eyebrow_tip_point.x * w)][int(eyebrow_tip_point.y * h)][1]) + b
#     return W, H, D


def cal_headcube(capture, point_list):
    image = capture[:, :, :3]
    h, w, c = image.shape
    nose_point = point_list[4]
    left_face_point = point_list[93]
    right_face_point = point_list[323]
    nose_bottom_point = point_list[2]
    eyebrow_tip_point = point_list[55]  # or 285
    a = int(w * 0.04)
    # b = int(h * 0.19)
    D1 = abs(capture[int(nose_point.y * h)][int(nose_point.x * w)][2]
             - capture[int(left_face_point.y * h)][int(left_face_point.x * w)][2])
    D2 = abs(capture[int(nose_point.y * h)][int(nose_point.x * w)][2]
             - capture[int(right_face_point.y * h)][int(right_face_point.x * w)][2])
    D = 2 * max(D1, D2)
    W1 = abs(int(nose_point.x * w) - int(left_face_point.x * w))
    W2 = abs(int(nose_point.x * w) - int(right_face_point.x * w))
    W = 2 * (max(W1, W2) + a)
    # H = 3 * abs(int(nose_bottom_point.y * h) - int(eyebrow_tip_point.y * h)) + b
    H = 3 * abs(int(nose_bottom_point.y * h) - int(eyebrow_tip_point.y * h)) + 30
    return W, H, D


def cal_headcube2(capture, point_list):
    image = capture[:, :, :3]
    h, w, c = image.shape
    nose_bottom_point = point_list[2]
    lm = []
    for p in point_list:
        lm.append([p.x, p.y])
    lm = np.array(lm)
    max = np.max(lm, axis=0)
    min = np.min(lm, axis=0)
    W = int((max[0] - min[0]) * w)
    H = int((max[1] - min[1]) * h)




'''
def cal_headcube_with_CS(capture, point_list):
    image = capture.transformed_color[:, :, :3]
    h, w, c = image.shape
    left_eye_mean_point = mean_point(point_list, left_eye_point)
    right_eye_mean_point = mean_point(point_list, right_eye_point)
    nose_point = point_list[4]
    left_face_point = point_list[93]
    right_face_point = point_list[323]
    nose_bottom_point = point_list[10]
    eyebrow_tip_point = point_list[55]

    x = capture.transformed_color[int(right_eye_mean_point.x * w)][int(right_eye_mean_point.y * h)] \
        - capture.transformed_color[int(left_eye_mean_point.x * w)][int(left_eye_mean_point.y * h)]
    t1 = capture.transformed_color[int(left_eye_mean_point.x * w)][int(left_eye_mean_point.y * h)] \
        - capture.transformed_color[int(nose_point.x * w)][int(nose_point.y * h)]
    t2 = capture.transformed_color[int(right_eye_mean_point.x * w)][int(right_eye_mean_point.y * h)] \
        - capture.transformed_color[int(nose_point.x * w)][int(nose_point.y * h)]
    y = np.cross(t1, t2)
    z = np.cross(x, y)
    x_nor = np.divide(x, math.sqrt(sum(e**2 for e in x)))
    y_nor = np.divide(y, math.sqrt(sum(e**2 for e in y)))
    z_nor = np.divide(z, math.sqrt(sum(e**2 for e in z)))
'''

def plt_show(points_list, colors_list, x=[-300, 300], y=[-300, 300], z=[0, 4000]):
    new_points = []
    new_colors = []
    for point, color in zip(points_list, colors_list):
        if any(point) and any(color):
            new_points.append(point)
            new_colors.append(color)
    new_points = np.array(new_points)
    new_colors = np.array(new_colors)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(
        new_points[:, 0], new_points[:, 1], new_points[:, 2], s=1, c=new_colors / 255,
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim(x[0], x[1])
    ax.set_ylim(y[0], y[1])
    ax.set_zlim(z[0], z[1])
    ax.view_init(elev=-90, azim=-90)
    plt.show()


def point_transform_CS(capture, landmark1, points1, colors1, landmark2, points2, colors2, face):
    image = capture[:, :, :3]
    h, w, c = image.shape
    nose_point1 = [int(landmark1[4][0] * w), int(landmark1[4][1] * h)]
    left_eye_mean_point = mean_point(landmark1, left_eye_point)
    left_eye_mean_point = [int(left_eye_mean_point[0] * w), int(left_eye_mean_point[1] * h)]
    right_eye_mean_point = mean_point(landmark1, right_eye_point)
    right_eye_mean_point = [int(right_eye_mean_point[0] * w), int(right_eye_mean_point[1] * h)]
    left_eyebrow_tip_point = [int(landmark1[55][0] * w), int(landmark1[55][1] * h)]
    right_eyebrow_tip_point = [int(landmark1[285][0] * w), int(landmark1[285][1] * h)]
    points1 = points1.reshape(h, w, 3)
    points2 = points2.reshape(h, w, 3)

    nose_point2 = [int(landmark2[4][0] * w), int(landmark2[4][1] * h)]
    if face == 'left':
        eye_mean_point = mean_point(landmark2, left_eye_point)
        eye_mean_point = [int(eye_mean_point[0] * w), int(eye_mean_point[1] * h)]
        eyebrow_tip_point = [int(landmark2[55][0] * w), int(landmark2[55][1] * h)]
        fullface_m = np.append(np.append(points1[nose_point1[1]][nose_point1[0]][:3],
                                         points1[left_eye_mean_point[1]][left_eye_mean_point[0]][:3], axis=0),
                               points1[left_eyebrow_tip_point[1]][left_eyebrow_tip_point[0]][:3], axis=0)
        fullface_m = np.array(fullface_m).reshape((3, 3))
        leftface_m = np.append(
            np.append(points2[nose_point2[1]][nose_point2[0]][:3], points2[eye_mean_point[1]][eye_mean_point[0]][:3],
                      axis=0),
            points2[eyebrow_tip_point[1]][eyebrow_tip_point[0]][:3], axis=0)
        leftface_m = np.array(leftface_m).reshape((3, 3))
        leftface_m_inv = np.linalg.inv(leftface_m)
        transform_m = np.matmul(fullface_m, leftface_m_inv)
    else:
        eye_mean_point = mean_point(landmark2, right_eye_point)
        eye_mean_point = [int(eye_mean_point[0] * w), int(eye_mean_point[1] * h)]
        eyebrow_tip_point = [int(landmark2[285][0] * w), int(landmark2[285][1] * h)]
        fullface_m = np.append(np.append(points1[nose_point1[1]][nose_point1[0]][:3],
                                         points1[right_eye_mean_point[1]][right_eye_mean_point[0]][:3], axis=0),
                               points1[right_eyebrow_tip_point[1]][right_eyebrow_tip_point[0]][:3], axis=0)
        fullface_m = np.array(fullface_m).reshape((3, 3))
        rightface_m = np.append(
            np.append(points2[nose_point2[1]][nose_point2[0]][:3], points2[eye_mean_point[1]][eye_mean_point[0]][:3],
                      axis=0),
            points2[eyebrow_tip_point[1]][eyebrow_tip_point[0]][:3], axis=0)
        rightface_m = np.array(rightface_m).reshape((3, 3))
        rightface_m_inv = np.linalg.inv(rightface_m)
        transform_m = np.matmul(fullface_m, rightface_m_inv)
    points1 = points1.reshape((-1, 3))
    points2 = points2.reshape((-1, 3))
    new_points = []
    new_colors = []
    i = 0
    for point2, color2 in zip(points2, colors2):
        if any(point2) and any(color2):
            print(i)
            i += 1
            tr_point2 = np.matmul(np.array(point2), transform_m)
            if points1.tolist().count(list(tr_point2)) < 1:
                points1 = np.append(points1, [tr_point2], axis=0)
                colors1 = np.append(colors1, [color2], axis=0)
                # points1.append(tr_point2)
                # colors1.append(color2)
    for point1, color1 in zip(points1, colors1):
        if any(point1) and any(color1):
            new_points.append(point1)
            new_colors.append(color1)
    new_points = np.array(new_points)
    new_colors = np.array(new_colors)
    return new_points, new_colors


# warnings.filterwarnings('ignore')

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

def main():
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_720P,
            camera_fps=pyk4a.FPS.FPS_5,
            depth_mode=pyk4a.DepthMode.WFOV_2X2BINNED,
            synchronized_images_only=True,
        )
    )
    k4a.start()

    # getters and setters directly get and set on device
    k4a.whitebalance = 4500
    assert k4a.whitebalance == 4500
    k4a.whitebalance = 4510
    assert k4a.whitebalance == 4510
    # while True:
    #     capture = k4a.get_capture()
    #     if np.any(capture.depth) and np.any(capture.color):
    #         break
    # while True:
    #     capture = k4a.get_capture()
    #     if np.any(capture.depth) and np.any(capture.color):
    #         break

    # points = capture.depth_point_cloud.reshape((-1, 3))
    # colors = capture.transformed_color[..., (2, 1, 0)].reshape((-1, 3))
    # cv2.imshow("k4adepth", colorize(capture.depth, (None, 5000), cv2.COLORMAP_HSV))
    data_file_id = 0
    while 1:
        capture = k4a.get_capture()
        if np.any(capture.depth) and np.any(capture.color):
            points = capture.depth_point_cloud.reshape((-1, 3))
            colors = capture.transformed_color[..., (2, 1, 0)].reshape((-1, 3))
            with mp_face_mesh.FaceMesh(
                    static_image_mode=True,
                    max_num_faces=1,
                    min_detection_confidence=0.5) as face_mesh:
                image = capture.transformed_color[:, :, :3]
                # image = capture.color[:, :, :3]
                results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                face_landmark_point = []
                for face_landmarks in results.multi_face_landmarks:
                    annotated_image = image.copy()
                    h, w, c = capture.transformed_color.shape
                    W, H, D = cal_headcube(capture.transformed_color, face_landmarks.landmark)
                    nose_bottom_point = [int(face_landmarks.landmark[2].x * w), int(face_landmarks.landmark[2].y * h)]

                    face_landmark_point.append([nose_bottom_point[0] - W // 2, nose_bottom_point[1] - 2 * H // 3])
                    face_landmark_point.append([nose_bottom_point[0] + W // 2, nose_bottom_point[1] - 2 * H // 3])
                    face_landmark_point.append([nose_bottom_point[0] + W // 2, nose_bottom_point[1] + H // 3])
                    face_landmark_point.append([nose_bottom_point[0] - W // 2, nose_bottom_point[1] + H // 3])
                # W, H, D = cal_headcube(capture.depth_point_cloud, face_landmarks.landmark)
                # nose_point = capture.depth_point_cloud[int(face_landmarks.landmark[4].x * w)][int(face_landmarks.landmark[4].y * h)]
                # print(nose_point)
                # x = [nose_point[0] - W // 2, nose_point[0] + W // 2]
                # y = [nose_point[1] - H // 3, nose_point[1] + 2 * H // 3]
                # z = [0, nose_point[2] + D]
                # print(x, y, z)
                # plt_show(points, colors)
                    # 还要获取一下鼻尖的坐标
                    # is_fullface(face_landmarks.landmark, left_eye_point, right_eye_point)
                    # nose_depth = capture.depth[int(face_landmarks.landmark[4].x * w)][int(face_landmarks.landmark[4].y * h)]
                    # print(capture.depth_point_cloud[int(face_landmarks.landmark[152].x * w)][int(face_landmarks.landmark[152].y * h)])
                    # print(capture.depth_point_cloud[int(face_landmarks.landmark[10].x * w)][int(face_landmarks.landmark[10].y * h)])

                    # xiaba_y = int(face_landmarks.landmark[152].y * h)
                    # print(xiaba_y)
                    # naomen_y = int(face_landmarks.landmark[10].y * h)
                    # print(naomen_y)
                    # left_face_depth = capture.depth[int(face_landmarks.landmark[93].x * w)][int(face_landmarks.landmark[93].y * h)] + 200

                    # xiaba_y2 = int(face_landmarks.landmark[149].y * h)
                    # print(xiaba_y, xiaba_y2)

                    # 鼻尖的深度值，脸部其他部位的深度值(左脸颊靠耳朵位置 234 93)
                    # print('1:', capture.depth_point_cloud[int(face_landmarks.landmark[4].x * w)][
                    #           int(face_landmarks.landmark[4].y * h)])  # [-192  -28  569]
                    # print('2:', capture.depth_point_cloud[int(face_landmarks.landmark[234].x * w)][
                    #           int(face_landmarks.landmark[234].y * h)])  # [-583 -280 1691]
                    # print('3:', capture.depth_point_cloud[int(face_landmarks.landmark[93].x * w)][
                    #           int(face_landmarks.landmark[93].y * h)])  # [-586 -308 1868]
                    lm_list = []
                    for id, lm in enumerate(face_landmarks.landmark):
                        lm_list.append([lm.x, lm.y])
                        if id == 4:
                            nose_xy = [int(lm.x * w), int(lm.y * h), lm.x, lm.y]
                        if id not in face_point+left_eye_point+right_eye_point:
                            face_landmarks.landmark[id].x = 0
                            face_landmarks.landmark[id].y = 0
                    # for i in face_point+left_eye_point+right_eye_point:
                    #     lm = face_landmarks.landmark[i]
                    #     cx, cy = int(lm.x * w), int(lm.y * h)
                    #     face_landmark_point.append([cx, cy])
                    annotated_image = image.copy()
                    mp_drawing.draw_landmarks(
                        image=annotated_image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACE_CONNECTIONS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec)
                    cv2.imshow("lmcolor1", annotated_image)

                    im = np.zeros(annotated_image.shape[:2], dtype=np.uint8)
                    cv2.fillPoly(im, np.array([face_landmark_point], dtype=np.int32), 255)
                    mask = im
                    masked = cv2.bitwise_and(image, image, mask=mask)
                    cv2.imshow("lmcolor2", masked)

            key = cv2.waitKey(10)
            if key == ord('0'):
                data_file_id += 1
                colors = masked[..., (2, 1, 0)].reshape((-1, 3))
                # np.save('C:/Users/10401/Desktop/ttt/data/points1_' + str(data_file_id) + '.npy', points)
                # np.save('C:/Users/10401/Desktop/ttt/data/colors1_' + str(data_file_id) + '.npy', colors)
                # print(capture.depth_point_cloud[nose_xy[1]][nose_xy[0]])
                # print(points[nose_xy[1] * w + nose_xy[0]])
                # # print(nose_bottom_point)
                # print(nose_xy)
                for id, point, color in zip(range(len(points)), points, colors):
                    if (any(point) or any(color)) and im[id // w][id % w] == 0:
                        points[id] = [0, 0, 0]
                        colors[id] = [0, 0, 0]
                # print(points[nose_xy[1]*w+nose_xy[0]])
                # print(capture.depth_point_cloud[nose_xy[1]][nose_xy[0]])
                # print(points.reshape(h, w, 3)[nose_xy[1]][nose_xy[0]])
                np.save('C:/Users/10401/Desktop/ttt/data/points_' + str(data_file_id) + '.npy', points)
                np.save('C:/Users/10401/Desktop/ttt/data/colors_' + str(data_file_id) + '.npy', colors)
                np.save('C:/Users/10401/Desktop/ttt/data/landmark_' + str(data_file_id) + '.npy', np.array(lm_list))
                cv2.imwrite('C:/Users/10401/Desktop/ttt/image_' + str(data_file_id) + '.png', annotated_image)
                print('---------------------------------------save ' + str(data_file_id))
            if key == ord('5'):
                cv2.destroyAllWindows()
                break
    k4a.stop()

    points1 = np.load('C:/Users/10401/Desktop/ttt/data/points_1.npy')
    colors1 = np.load('C:/Users/10401/Desktop/ttt/data/colors_1.npy')
    landmark1 = np.load('C:/Users/10401/Desktop/ttt/data/landmark_1.npy')
    points2 = np.load('C:/Users/10401/Desktop/ttt/data/points_2.npy')
    colors2 = np.load('C:/Users/10401/Desktop/ttt/data/colors_2.npy')
    landmark2 = np.load('C:/Users/10401/Desktop/ttt/data/landmark_2.npy')
    points3 = np.load('C:/Users/10401/Desktop/ttt/data/points_3.npy')
    colors3 = np.load('C:/Users/10401/Desktop/ttt/data/colors_3.npy')
    landmark3 = np.load('C:/Users/10401/Desktop/ttt/data/landmark_3.npy')
    # plt_show(points1, colors1)
    # plt_show(points2, colors2)
    # plt_show(points3, colors3)
    # points1 = np.load('C:/Users/10401/Desktop/ttt/data/points1_1.npy')
    # colors1 = np.load('C:/Users/10401/Desktop/ttt/data/colors1_1.npy')
    # plt_show(points1, colors1)
    print('--------------------processing------------')
    new_points, new_colors = point_transform_CS(capture.transformed_color, landmark1, points1, colors1, landmark2, points2, colors2, 'right')
    new_points, new_colors = point_transform_CS(capture.transformed_color, landmark1, new_points, new_colors, landmark3, points3, colors3, 'left')
    print('--------------------showing-----------------')
    plt_show(new_points, new_colors)
'''
    new_points = []
    new_colors = []
    for id, point, color in zip(range(len(points)), points, colors):
        # if any(point) and any(color) and im[id // annotated_image.shape[1]][id % annotated_image.shape[1]]:
        #     new_points.append(point) and point[1] >= xiaba_y
        #     new_colors.append(color)
        if any(point) and any(color) and point[2] >= nose_depth:
            new_points.append(point)
            new_colors.append(color)

    new_points = np.array(new_points)
    new_colors = np.array(new_colors)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(
        new_points[:, 0], new_points[:, 1], new_points[:, 2], s=1, c=new_colors / 255,
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim(-300, 300)
    ax.set_ylim(-300, 300)
    ax.set_zlim(0, 3000)
    ax.view_init(elev=-90, azim=-90)
    plt.show()

    k4a.stop()
'''

if __name__ == "__main__":
    main()
