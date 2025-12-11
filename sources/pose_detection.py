import threading

import cv2
import numpy as np
import winsound


def angle_3d(a, b, c):
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

org1 = (520,100)
org2 = (50,900)
font = cv2.FONT_HERSHEY_SIMPLEX
thickness = 3
font_scale = 2
text_format = "LOW CONFIDENCE Squats: 100 "

def paint_squats_on_display(frame,val1,val2,color):
    cv2.putText(frame,
                f"{val1} Squats: {val2}",
                org1,
                font,
                2,
                color,
                3)

def paint_on_display(frame,org):
    (text_w,text_h),baseline = cv2.getTextSize(text_format,font,font_scale,thickness)
    cv2.rectangle(frame,
                  (org[0] - 10, org[1] -text_h- 10),
                  (org[0] + text_w +  10, org[1] +baseline + 10),
                  (30,30,30),
                  -1)

def paint_text_on_display(frame,text,org):
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    cv2.rectangle(frame,
                  (org[0] - 10, org[1] - text_h - 10),
                  (org[0] + text_w + 10, org[1] + baseline + 10),
                  (30, 30, 30),
                  -1)

    cv2.putText(frame,
                text,
               org2,
                font,
                2,
                (0,255,0),
                3)


def detect_squats(main_body):
    # right_knee = main_body.keypoint[9]
    # right_hip = main_body.keypoint[8]
    # right_ankle = main_body.keypoint[10]
    right_knee = main_body.keypoint[23]
    right_hip = main_body.keypoint[22]
    right_ankle = main_body.keypoint[24]
    knee_angle = angle_3d(right_hip, right_knee, right_ankle)
    return knee_angle


def verify_confidence(main_body) -> bool:
    return main_body.keypoint_confidence[9] > 0.3 and main_body.keypoint_confidence[8] > 0.3 and main_body.keypoint_confidence[10] > 0.3

def play_beep_async():
    threading.Thread(target=lambda: winsound.Beep(700, 500), daemon=True).start()



class Squat:
    def __init__(self):
        self.state = "S0"
        self.angle = 180
        self.squat_counter = 0
        self.rep_made = 0
        self.message = "Start"
        

    def paint(self,image_left_ocv,main_body):
        if main_body.keypoint_confidence[9] > 0.3 and main_body.keypoint_confidence[8] > 0.3 and \
                main_body.keypoint_confidence[10] > 0.3:

            paint_on_display(image_left_ocv,org1)
            paint_squats_on_display(image_left_ocv, f"Angle: {int(self.angle)}", self.squat_counter, (0, 255, 0))


        else:
            paint_on_display(image_left_ocv,org1)
            paint_squats_on_display(image_left_ocv, "LOW CONFIDENCE", self.squat_counter, (0, 0, 255))

        if self.state == "S0":
            paint_text_on_display(image_left_ocv,self.message,org2)

    def detect(self, main_body):
        if verify_confidence(main_body):
            self.angle = detect_squats(main_body)
            if self.state == "S0":

                if self.rep_made == 1:
                    self.squat_counter = self.squat_counter + 1
                    self.rep_made = 0 #Resetam repetarea
                if self.angle < 130:
                    self.state = "S1"

            #Starea intermediara
            elif self.state == "S1":
                if self.angle < 90:
                    self.state = "S2"
                elif self.angle > 130:
                    self.state = "S0"
                    if self.rep_made == 0:
                        self.message = "You should go deeper"
                elif self.angle > 90 and self.rep_made==0 :
                    self.message = "Go deeper"

            #starea finala
            elif self.state == "S2":
                self.rep_made = 1
                if self.angle > 90:
                    self.state = "S1"
                    self.message = "Good Job"
                    play_beep_async()