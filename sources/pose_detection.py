import cv2
import numpy as np

state = "STAND"
squat_count = 0


def angle_3d(a, b, c):
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))


def detect_squats(image_left_ocv,main_body):
    global squat_count, state

    font = cv2.FONT_HERSHEY_SIMPLEX
    if main_body.keypoint_confidence[9] > 0.3 and main_body.keypoint_confidence[8] > 0.3 and main_body.keypoint_confidence[10] > 0.3:
        right_knee = main_body.keypoint[9]
        right_hip = main_body.keypoint[8]
        right_ankle = main_body.keypoint[10]

        knee_angle = angle_3d(right_hip, right_knee, right_ankle)
        if state == "STAND" and knee_angle < 90:
            state = "SQUAT"

        if state == "SQUAT" and knee_angle > 150:
            state = "STAND"
            squat_count += 1

        cv2.putText(image_left_ocv,
                    f"Angle: {int(knee_angle)}° Squats: {squat_count}",
                    (50, 150),
                    font,
                    2,
                    (0, 255, 0),
                    3)
    else:
        cv2.putText(image_left_ocv,
                    "LOW CONFIDENCE",
                    (50, 150),
                   font,
                    2,
                    (0, 0, 255),
                    3)