import numpy as np

def angle_3d(a, b, c):
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

def compute_arm_angles(main_body):

    left_shoulder = main_body.keypoint[5]
    left_elbow = main_body.keypoint[6]
    left_hip = main_body.keypoint[18]

    right_shoulder = main_body.keypoint[12]
    right_elbow = main_body.keypoint[13]
    right_hip = main_body.keypoint[22]

    left_arm_angle = angle_3d(left_elbow, left_shoulder, left_hip)
    right_arm_angle = angle_3d(right_elbow, right_shoulder, right_hip)
    return left_arm_angle, right_arm_angle


def compute_legs_angle(main_body):

    pelvis = main_body.keypoint[0]
    left_ankle = main_body.keypoint[20]
    right_ankle = main_body.keypoint[24]

    legs_angle = angle_3d(left_ankle, pelvis, right_ankle)
    return legs_angle


def verify_confidence(main_body) -> bool:
    return (main_body.keypoint_confidence[5] > 0.3 and
            main_body.keypoint_confidence[12] > 0.3 and
            main_body.keypoint_confidence[20] > 0.3 and
            main_body.keypoint_confidence[24] > 0.3)