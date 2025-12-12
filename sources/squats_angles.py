import threading

import cv2
import numpy as np
import winsound


def angle_3d(a, b, c):
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))



def compute_knee_angle(main_body):
    # right_knee = main_body.keypoint[9]
    # right_hip = main_body.keypoint[8]
    # right_ankle = main_body.keypoint[10]

    right_knee = main_body.keypoint[23]
    right_hip = main_body.keypoint[22]
    right_ankle = main_body.keypoint[24]

    right_knee_angle = angle_3d(right_hip, right_knee, right_ankle)

    left_knee = main_body.keypoint[19]
    left_hip = main_body.keypoint[18]
    left_ankle = main_body.keypoint[20]
    left_knee_angle = angle_3d(left_hip, left_knee, left_ankle)



    return left_knee_angle,right_knee_angle


def compute_back_angle(main_body):

    # pelvis = main_body.keypoint[0]
    # neck = main_body.keypoint[3]
    # right_knee = main_body.keypoint[23]
    #
    # back_angle = angle_3d(neck,pelvis,right_knee)
    #

    pelvis = main_body.keypoint[0]
    neck = main_body.keypoint[3]
    perpendicular_point = np.array([pelvis[0],1,pelvis[2]])

    back_angle = angle_3d(neck,pelvis,perpendicular_point)

    return back_angle


def verify_confidence(main_body) -> bool:
    return main_body.keypoint_confidence[22] > 0.3 and main_body.keypoint_confidence[23] > 0.3 and main_body.keypoint_confidence[24] > 0.3







