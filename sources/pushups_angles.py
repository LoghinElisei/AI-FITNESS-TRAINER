import threading

import cv2
import numpy as np
import winsound


def angle_3d(a, b, c):
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))


def compute_elbow_angle(main_body):
    # right_knee = main_body.keypoint[9]
    # right_hip = main_body.keypoint[8]
    # right_ankle = main_body.keypoint[10]

    right_elbow = main_body.keypoint[13]
    right_wrist = main_body.keypoint[14]
    right_shoulder = main_body.keypoint[12]

    right_elbow_angle = angle_3d(right_wrist,right_elbow, right_shoulder)

    left_elbow = main_body.keypoint[6]
    left_wrist = main_body.keypoint[7]
    left_shoulder = main_body.keypoint[5]
    left_elbow_angle = angle_3d(left_wrist,left_elbow, left_shoulder)

    return left_elbow_angle, right_elbow_angle


def compute_back_angle(main_body):

    left_ankle = main_body.keypoint[20]
    back = main_body.keypoint[1]
    left_shoulder = main_body.keypoint[5]
    back_angle = angle_3d(left_ankle,back,left_shoulder)

    return back_angle


def verify_confidence(main_body) -> bool:
    return main_body.keypoint_confidence[20] > 0.3 and main_body.keypoint_confidence[1] > 0.3 and main_body.keypoint_confidence[5] > 0.3

#
#
# def compute_elbow_angle(main_body):
#     # right_knee = main_body.keypoint[9]
#     # right_hip = main_body.keypoint[8]
#     # right_ankle = main_body.keypoint[10]
#
#     right_elbow = main_body.keypoint[3]
#     right_wrist = main_body.keypoint[4]
#     right_shoulder = main_body.keypoint[2]
#
#     right_elbow_angle = angle_3d(right_wrist,right_elbow, right_shoulder)
#
#     left_elbow = main_body.keypoint[6]
#     left_wrist = main_body.keypoint[7]
#     left_shoulder = main_body.keypoint[5]
#     left_elbow_angle = angle_3d(left_wrist,left_elbow, left_shoulder)
#
#     print("left_elbow_angle ",left_elbow_angle)
#     print("right_elbow_angle ",right_elbow_angle)
#     return left_elbow_angle, right_elbow_angle
#
#
# def compute_back_angle(main_body):
#
#     left_ankle = main_body.keypoint[13]
#     back = main_body.keypoint[11]
#     left_shoulder = main_body.keypoint[5]
#     back_angle = angle_3d(left_ankle,back,left_shoulder)
#
#     return back_angle
#
#
# def verify_confidence(main_body) -> bool:
#     return main_body.keypoint_confidence[8] > 0.3 and main_body.keypoint_confidence[11] > 0.3 and main_body.keypoint_confidence[1] > 0.3
#
#
#

