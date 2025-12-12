from GUI import *
from squats_angles import *
from verify import *

class Squat:
    def __init__(self):
        self.state = "S0"
        self.knee_angle = 180
        self.back_angle = 180
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
            paint_rep_on_display(image_left_ocv, f"Knee Angle: {int(self.knee_angle)}","Squats", (0, 255, 0))
            paint(image_left_ocv,f"CORRECT : {self.correct} ",org3,color=(255,255,255),background_color=(0,255,0))
            paint(image_left_ocv, f"INCORRECT : {self.incorrect} ", org4,color=(255,255,255),background_color=(0,0,255))
            paint(image_left_ocv, f"Back Angle: {int(self.back_angle)}", org6,color=(0,255,0),background_color=(0,0,0))

        else:
            paint_on_display_background(image_left_ocv,org1)
            paint_rep_on_display(image_left_ocv, "LOW CONFIDENCE","Squats", (0, 0, 255))

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
                            if self.back_angle > 45:
                                self.message="BEND BACKWARDS"
                                self.wrong_movement = True

                            else:
                                if self.wrong_movement:
                                    self.incorrect +=1
                                    self.wrong_movement = False
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
                        if self.back_angle > 45:
                            self.message = "BEND BACKWARDS"
                            self.wrong_movement = True
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
                        if self.back_angle > 45:
                            self.message = "BEND BACKWARDS"
                            self.wrong_movement = True
                        if self.last_state != "S2":
                            self.state_queue.append("S2")
                            self.last_state = "S2"

                        if self.knee_angle > 90:
                            self.state = "S1"
                            play_beep_async()

    def verify_movement(self,main_body):
       pass