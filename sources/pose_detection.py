import cv2
import numpy as np

state = "STAND"
squat_count = 0


def angle_3d(a, b, c):
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

org = (520,100)
font = cv2.FONT_HERSHEY_SIMPLEX
thickness = 3
font_scale = 2
text_format = "LOW CONFIDENCE Squats: 100 "

def paint_text_on_display(frame,val1,val2,color):

    cv2.putText(frame,
                f"{(val1)} Squats: {val2}",
                org,
                font,
                2,
                color,
                3)

def paint_on_display(frame):
    (text_w,text_h),baseline = cv2.getTextSize(text_format,font,font_scale,thickness)
    cv2.rectangle(frame,
                  (org[0] - 10, org[1] -text_h- 10),
                  (org[0] + text_w +  10, org[1] +baseline + 10),
                  (30,30,30),
                  -1)

def detect_squats(image_left_ocv,main_body):
    global squat_count, state


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

        paint_on_display(image_left_ocv)
        paint_text_on_display(image_left_ocv,f"Angle: {int(knee_angle)}",squat_count,(0, 255, 0))
    else:
        paint_on_display(image_left_ocv)
        paint_text_on_display(image_left_ocv, "LOW CONFIDENCE",squat_count, (0, 0, 255))
