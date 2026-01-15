from GUI import *
from squats_angles import *
from verify import *

class Squat:
    def __init__(self):
        self.state = "S0"
        self.knee_angle = 180
        self.back_angle = 180
        self.message = "Start"
        self.message_template =[colorRed,colorWhite] # [background, text]
        self.message_state = "STANDING"
        # self.feedback_message = "Start"
        self.state_queue = []
        self.wrong_movement = False
        self.correct = 0
        self.incorrect = 0
        self.last_state = "S0"

    def reset(self):
        self.correct = 0
        self.incorrect = 0

    def paint(self,image_left_ocv,main_body):
        paint(image_left_ocv,"SQUATS",orgTitle,color=(252, 34, 0),bg_color = (14,201, 255))
        draw_command_menu(image_left_ocv,orgCommands)
        paint(image_left_ocv, f"CORRECT: {self.correct}  ", orgCorrect, color=(255, 255, 255), bg_color=(0, 255, 0))
        paint(image_left_ocv, f"INCORRECT: {self.incorrect}", orgIncorrect, color=(255, 255, 255), bg_color=(0, 0, 255))
        paint(image_left_ocv, f"Back Angle: {int(self.back_angle)}", orgInfo1, color=(0, 255, 0), bg_color=(0, 0, 0))
        paint(image_left_ocv, f"Knee Angle: {int(self.knee_angle)}", orgInfo2, color=(0, 255, 0), bg_color=(0, 0, 0))
        paint(image_left_ocv, f"STATE: {self.message_state}", orgState, colorBlack, colorTurquoise)
        if self.message == "BODY NOT FULLY DETECTED":
            self.message = ""

        if not verify_confidence(main_body):
            # paint_on_display_background(image_left_ocv,org1)
            # paint_rep_on_display(image_left_ocv, "LOW CONFIDENCE","Squats", (0, 0, 255))
            paint(image_left_ocv, "LOW CONFIDENCE", org1, color=(0, 0, 255), bg_color=(0, 0, 0))
            self.message = "BODY NOT FULLY DETECTED"
            self.message_template = [colorRed, colorWhite]
        if self.message != "":
            paint(image_left_ocv, self.message, orgAttention, self.message_template[1], self.message_template[0])


    def detect(self, main_body):
            if verify_confidence(main_body):
                left_knee_angle, right_knee_angle = compute_knee_angle(main_body)
                self.back_angle = compute_back_angle(main_body)

                if abs(left_knee_angle - right_knee_angle) < 50:

                    self.knee_angle = right_knee_angle

                    if self.state == "S0":
                        self.message_state = "STANDING"
                        if len(self.state_queue) == 0:
                            if self.back_angle > 42:
                                self.message= "IMPROPER BACK POSTURE"
                                self.message_template = [colorRed, colorWhite]
                                self.wrong_movement = True

                            else:
                                if self.wrong_movement:
                                    self.incorrect +=1
                                    self.wrong_movement = False
                                # self.message= ""
                            if self.knee_angle < 130:
                                self.state = "S1"
                                self.last_state = "S0"
                                self.message_state = "DESCENT"
                        else:
                            if exercises_is_correct(self.state_queue) and self.wrong_movement == False:
                                self.correct +=1
                                self.message = "GOOD JOB"
                                self.message_template = [colorGreen, colorWhite]
                                play_beep_async()
                            else:
                                self.incorrect +=1
                                play_beep_async(error=True)

                            self.state_queue = []
                            self.wrong_movement = False


                    #Starea intermediara
                    elif self.state == "S1":
                        if 20 > self.back_angle > 55:
                            self.message = "IMPROPER BACK POSTURE"
                            self.wrong_movement = True
                            self.message_template = [colorRed, colorWhite]
                        if self.knee_angle < 90:
                            self.state = "S2"
                            self.state_queue.append("S1")
                            self.last_state = "S1"
                            self.message_state = "BOTTOM"
                            self.message="GO UP"
                            self.message_template = [colorYellow,colorBlack]

                        elif self.knee_angle > 130:
                            self.state = "S0"
                            self.state_queue.append("S1")
                            self.last_state = "S1"

                        if self.last_state == "S0":
                            self.message= "GO DOWN"
                            self.message_template = [colorYellow,colorBlack]
                        # else:
                        #     self.message= ""

                    #starea finala
                    elif self.state == "S2":
                        if self.back_angle > 65:
                            self.message = "IMPROPER BACK POSTURE"
                            self.message_template = [colorRed, colorWhite]
                            self.wrong_movement = True
                            play_beep_async(error=True)
                        if self.last_state != "S2":
                            self.state_queue.append("S2")
                            self.last_state = "S2"

                        if self.knee_angle > 90:
                            self.message_state = "ASCENT"
                            self.state = "S1"


    def verify_movement(self,main_body):
       pass