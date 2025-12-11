import threading

import cv2
import numpy as np
import winsound


def angle_3d(a, b, c):
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))


import cv2

# --- Globalele tale (Constante) ---
org1 = (520, 100)
org2 = (50, 900)
org3 = (1200, 300)
org4 = (1200, 400)
org5 = (20,1000)
org6 = (520,200)
font = cv2.FONT_HERSHEY_SIMPLEX
thickness = 3
font_scale = 2
text_format = "LOW CONFIDENCE Squats: 100 "


def _draw_text_with_bg(frame, text, org, color, bg_color):

    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    x, y = org
    padding = 10

    cv2.rectangle(frame,
                  (x - padding, y - text_h - padding),  # Stânga-Sus
                  (x + text_w + padding, y + baseline + padding),  # Dreapta-Jos
                  bg_color,
                  -1)

    # 3. Desenăm textul peste dreptunghi
    cv2.putText(frame,
                text,
                org,
                font,
                font_scale,
                color,
                thickness)


def paint_squats_on_display(frame, val1, val2, color):

    text = f"{val1} Squats: {val2}"
    _draw_text_with_bg(frame, text, org1, color, (30, 30, 30))


def paint(frame, text, org, color, background_color):
    _draw_text_with_bg(frame, text, org, color, background_color)


# --- Funcții Vechi (păstrate pentru compatibilitate, dar reparate) ---

def paint_on_display_background(frame, org):


    (text_w, text_h), baseline = cv2.getTextSize(text_format, font, font_scale, thickness)
    cv2.rectangle(frame,
                  (org[0] - 10, org[1] - text_h - 10),
                  (org[0] + text_w + 10, org[1] + baseline + 10),
                  (30, 30, 30),
                  -1)


def paint_text_on_display(frame, text, org):
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    cv2.rectangle(frame,
                  (org[0] - 10, org[1] - text_h - 10),
                  (org[0] + text_w + 10, org[1] + baseline + 10),
                  (30, 30, 30),
                  -1)


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
    perpendicular_point = np.array([pelvis[0],neck[1],pelvis[2]])

    back_angle = angle_3d(neck,pelvis,perpendicular_point)

    return back_angle



def verify_confidence(main_body) -> bool:
    return main_body.keypoint_confidence[9] > 0.3 and main_body.keypoint_confidence[8] > 0.3 and main_body.keypoint_confidence[10] > 0.3

def play_beep_async():
    threading.Thread(target=lambda: winsound.Beep(700, 500), daemon=True).start()


def exercises_is_correct(queue:list)->bool:
    #for correct exercises, we must have [S1,S2,S1]
    if len(queue) == 3:
        print(f"******** BRAVO {queue} *******")
        return True
    else:
        return False



class Squat:
    def __init__(self):
        self.state = "S0"
        self.knee_angle = 180
        self.back_angle = 180
        self.squat_counter = 0
        self.rep_made = 0
        self.message = "Start"
        self.state_queue = []
        self.wrong_movement = False
        self.correct = 0
        self.incorrect = 0
        self.last_state = "S0"

    def paint(self,image_left_ocv,main_body):
        if main_body.keypoint_confidence[9] > 0.3 and main_body.keypoint_confidence[8] > 0.3 and \
                main_body.keypoint_confidence[10] > 0.3:

            paint_on_display_background(image_left_ocv,org1)
            paint_squats_on_display(image_left_ocv, f"Knee Angle: {int(self.knee_angle)}", self.squat_counter, (0, 255, 0))
            paint(image_left_ocv,f"CORRECT : {self.correct} ",org3,color=(255,255,255),background_color=(0,255,0))
            paint(image_left_ocv, f"INCORRECT : {self.incorrect} ", org4,color=(255,255,255),background_color=(0,0,255))
            paint(image_left_ocv, f"Back Angle: {int(self.back_angle)}", org6,color=(0,255,0),background_color=(0,0,0))

        else:
            paint_on_display_background(image_left_ocv,org1)
            paint_squats_on_display(image_left_ocv, "LOW CONFIDENCE", self.squat_counter, (0, 0, 255))

        if self.message != "":
            paint(image_left_ocv, self.message, org5,color=(255,255,255),background_color=(0,0,255))



    def detect(self, main_body):
            if verify_confidence(main_body):

                left_knee_angle, right_knee_angle = compute_knee_angle(main_body)
                self.back_angle = compute_back_angle(main_body)

                if abs(left_knee_angle - right_knee_angle) < 50:

                    self.knee_angle = right_knee_angle

                    if self.state == "S0":

                        if len(self.state_queue) == 0:
                            if self.back_angle > 50:
                                self.message="BEND BACKWARDS"
                                self.wrong_movement = True
                            else:
                                self.message=""
                            if self.knee_angle < 130:
                                self.state = "S1"
                                self.last_state = "S0"
                        else:
                            if exercises_is_correct(self.state_queue) and self.wrong_movement == False:
                                self.correct +=1
                            else:
                                self.incorrect +=1

                            self.state_queue = []
                            self.wrong_movement = False


                    #Starea intermediara
                    elif self.state == "S1":
                        # if self.last_state != "S1":
                        #     self.state_queue.append("S1")
                        #     self.last_state = "S1"

                        if self.knee_angle < 90:
                            self.state = "S2"
                            self.state_queue.append("S1")
                            self.last_state = "S1"

                        elif self.knee_angle > 130:
                            self.state = "S0"
                            self.state_queue.append("S1")
                            self.last_state = "S1"

                        if self.last_state == "S0":
                            self.message="Go Deeper"
                        else:
                            self.message=""

                    #starea finala
                    elif self.state == "S2":
                        if self.last_state != "S2":
                            self.state_queue.append("S2")
                            self.last_state = "S2"

                        if self.knee_angle > 90:
                            self.state = "S1"
                            play_beep_async()

    def verify_movement(self,main_body):
       pass