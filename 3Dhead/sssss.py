import cv2
import mediapipe as mp
import math
import numpy as np


face_point = [234, 127, 162, 21, 54, 103, 67, 109, 10, 338, 297, 332, 284, 251, 389, 93, 132, 58, 138, 172, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 397, 288, 361, 323, 454, 356]
left_eye_point = [7, 33, 246, 160, 161, 159, 158, 157, 133, 155, 173, 154, 153, 145, 144, 163]
right_eye_point = [362, 382, 398, 384, 385, 386, 387, 263, 388, 466, 249, 390, 373, 374, 380, 381]


def caozuoyixia(l):
    bool_list = []
    for id1, lm1 in enumerate(face_landmarks.landmark):
        flag = True
        if lm1.x <= 0.5 and lm1.y <= 0.5:
            for id2, lm2 in enumerate(face_landmarks.landmark):
                if lm2.x < lm1.x and lm2.y < lm1.y:
                    bool_list.append(False)
                    flag = False
                    break
        elif lm1.x < 0.5 and lm1.y > 0.5:
            for id2, lm2 in enumerate(face_landmarks.landmark):
                if lm2.x < lm1.x and lm2.y > lm1.y:
                    bool_list.append(False)
                    flag = False
                    break
        elif lm1.x > 0.5 and lm1.y < 0.5:
            for id2, lm2 in enumerate(face_landmarks.landmark):
                if lm2.x > lm1.x and lm2.y < lm1.y:
                    bool_list.append(False)
                    flag = False
                    break
        else:
            for id2, lm2 in enumerate(face_landmarks.landmark):
                if lm2.x > lm1.x and lm2.y > lm1.y:
                    bool_list.append(False)
                    flag = False
                    break
        if flag:
            bool_list.append(True)
    return bool_list


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


def findSubStrIndex(substr, s, time):
    str = str(s)
    i = 0
    index = -1
    while i < time:
        index = str.find(substr, index+1)
        i+=1
    return index


def panduan(point, p_l):
    for p in p_l:
        if pow(abs(p[0] - point[0]), 2) + pow(abs(p[1] - point[1]), 2) < 50:
            return True
    return False


mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# For static images:
IMAGE_FILES = ['C:/Users/10401/Desktop/ttt/xjj.jpg']
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    min_detection_confidence=0.8) as face_mesh:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    w, h, c = image.shape
    image = cv2.resize(image, (5*w, 5*h))
    # Convert the BGR image to RGB before processing.
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print and draw face mesh landmarks on the image.
    if not results.multi_face_landmarks:
      continue
    annotated_image = image.copy()
    h, w, c = annotated_image.shape

    right_point = [[684, 328], [695, 318], [709, 312], [722, 312], [734, 313], [744, 318], [750, 321], [744, 327], [738, 330], [728, 333], [716, 332], [706, 333], [695, 330]]
    left_point = [[539, 319], [548, 315], [554, 312], [568, 309], [579, 311], [592, 316], [600, 323], [603, 328], [605, 329], [594, 330], [583, 332], [574, 334], [559, 331], [551, 329], [550, 325]]

    for face_landmarks in results.multi_face_landmarks:
      # W, H, D = cal_headcube(image, face_landmarks.landmark)
      # nose_bottom_point = [int(face_landmarks.landmark[2].x * w), int(face_landmarks.landmark[2].y * h)]
      # face_landmark_point = []
      # face_landmark_point.append([nose_bottom_point[0] - W // 2, nose_bottom_point[1] - 2 * H // 3])
      # face_landmark_point.append([nose_bottom_point[0] + W // 2, nose_bottom_point[1] - 2 * H // 3])
      # face_landmark_point.append([nose_bottom_point[0] + W // 2, nose_bottom_point[1] + H // 3])
      # face_landmark_point.append([nose_bottom_point[0] - W // 2, nose_bottom_point[1] + H // 3])
      # print(face_landmark_point)
      # im = np.zeros(annotated_image.shape[:2], dtype=np.uint8)
      # print(im.shape)
      # cv2.fillPoly(im, np.array([face_landmark_point], dtype=np.int32), 255)
      # mask = im
      # masked = cv2.bitwise_and(image, image, mask=mask)
      # cv2.imshow("lmcolor2", masked)
      # bool_list = caozuoyixia(face_landmarks.landmark)
      # face_landmarks.landmark[151].y = 0.2
      for id, lm in enumerate(face_landmarks.landmark):
          # if id == 0:
          #     print(type(face_landmarks))
          # if lm.x < 0.42 or lm.x > 0.58 or lm.y < 0.35 or lm.y > 0.742:
          # if bool_list[id] and (id not in queding_point):
          # if abs(lm.x - 0.39401) < 0.01 and abs(lm.y - 0.5747509) < 0.01 and id not in queding_point:
          # if lm.y > 0.424 and lm.y < 0.47:
          cx, cy = int(lm.x * w), int(lm.y * h)
          # cv2.putText(annotated_image, str(int(id)), (cx, cy + 2), cv2.FONT_HERSHEY_PLAIN,
          #             1, (0, 0, 255), 1)
          # if cx > 520 and cx < 757 and cy > 300 and cy < 322 and panduan([cx, cy], left_point) :
          # if id == 61 or id == 78 or id == 146 or id == 185 or id == 191 or id == 95 or id == 40 or id == 88 or id == 80:
          if id == 82 or id == 87:
          # if pow(abs(cx - 1581), 2) + pow(abs(cy - 1632), 2) < 500:
          # if abs(lm.x - face_landmarks.landmark[4].x) < 0.0003 and abs(cy - face_landmarks.landmark[4].y * h) < 25:
          # if id in right_eye_point or id in left_eye_point:
              print(id, lm)
              # cx, cy = int(lm.x * w), int(lm.y * h)
              cv2.putText(annotated_image, str(int(id)), (cx + 2, cy + 2), cv2.FONT_HERSHEY_PLAIN,
                          1, (0, 0, 255), 1)
          else:
              face_landmarks.landmark[id].x = 0
              face_landmarks.landmark[id].y = 0
          # if id in face_point:
          #   print(id, lm)
          #   h, w, c = annotated_image.shape
          #   cx, cy = int(lm.x * w), int(lm.y * h)
          #   cv2.putText(annotated_image, str(int(id)), (cx + 2, cy + 2), cv2.FONT_HERSHEY_PLAIN,
          #               1, (0, 0, 255), 1)
          # else:
          #     face_landmarks.landmark[id].x = 0
          #     face_landmarks.landmark[id].y = 0
      mp_drawing.draw_landmarks(
          image=annotated_image,
          landmark_list=face_landmarks,
          connections=mp_face_mesh.FACE_CONNECTIONS,
          landmark_drawing_spec=drawing_spec,
          connection_drawing_spec=drawing_spec)
      cv2.imwrite('C:/Users/10401/Desktop/ttt/' + str(idx) + '9.png', annotated_image)
      # pos1 = findSubStrIndex('x: ', face_landmarks, 1)
      # print(pos1)
      # print('face_landmarks:', face_landmarks)

    #   mp_drawing.draw_landmarks(
    #       image=annotated_image,
    #       landmark_list=face_landmarks,
    #       connections=mp_face_mesh.FACE_CONNECTIONS,
    #       landmark_drawing_spec=drawing_spec,
    #       connection_drawing_spec=drawing_spec)
    # cv2.imwrite('C:/Users/lee/Pictures/Camera Roll/' + str(idx) + '.png', annotated_image)


