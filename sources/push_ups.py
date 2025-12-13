from GUI import *
from pushups_angles import *
from verify import *
class PushUps:
    def __init__(self):
        self.state = "S0"
        self.elbow_angle = 180
        self.back_angle = 180
        self.message = "Start"
        self.state_queue = []
        self.wrong_movement = False
        self.correct = 0
        self.incorrect = 0
        self.last_state = "S0"

    def paint(self,image_left_ocv,main_body):
        if verify_confidence(main_body):
            paint_on_display_background(image_left_ocv,org1)
            paint_rep_on_display(image_left_ocv, f"Elbow Angle: {int(self.elbow_angle)}", "Push-ups", (0, 255, 0))
            paint(image_left_ocv,f"CORRECT : {self.correct} ",org3,color=(255,255,255),background_color=(0,255,0))
            paint(image_left_ocv, f"INCORRECT : {self.incorrect}", org4,color=(255,255,255),background_color=(0,0,255))
            paint(image_left_ocv, f"Back Angle: {int(self.back_angle)}", org6,color=(0,255,0),background_color=(0,0,0))

        else:
            paint_on_display_background(image_left_ocv,org1)
            paint_rep_on_display(image_left_ocv, "LOW CONFIDENCE","Push-ups", (0, 0, 255))

        if self.message != "":
            paint(image_left_ocv, self.message, org5,color=(255,255,255),background_color=(0,0,255))



    def detect(self, main_body):
            if verify_confidence(main_body):

                left_elbow_angle,right_elbow_angle = compute_elbow_angle(main_body)
                self.back_angle = compute_back_angle(main_body)
                self.elbow_angle = right_elbow_angle
                if abs(left_elbow_angle - right_elbow_angle) < 50:



                    if self.state == "S0":
                        if len(self.state_queue) == 0:

                            # if self.back_angle > 45:
                            # #     self.message="BEND BACKWARDS"
                            # #     self.wrong_movement = True
                            #     pass
                            #
                            #
                            # else:
                            #     if self.wrong_movement:
                            #         self.incorrect +=1
                            #         self.wrong_movement = False
                            #     self.message=""
                            if self.elbow_angle < 150:
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
                        # if self.back_angle > 45:
                        #     self.message = "BEND BACKWARDS"
                        #     self.wrong_movement = True
                        if self.elbow_angle < 90:
                            self.state = "S2"
                            self.state_queue.append("S1")
                            self.last_state = "S1"

                        elif self.elbow_angle > 150:
                            self.state = "S0"
                            self.state_queue.append("S1")
                            self.last_state = "S1"

                        if self.last_state == "S0":
                            self.message="Go Deeper"
                        else:
                            self.message=""

                    #starea finala
                    elif self.state == "S2":
                        # if self.back_angle > 45:
                        #     self.message = "BEND BACKWARDS"
                        #     self.wrong_movement = True
                        if self.last_state != "S2":
                            self.state_queue.append("S2")
                            self.last_state = "S2"

                        if self.elbow_angle > 90:
                            self.state = "S1"
                            play_beep_async()
                else:
                    print("DIFERENTA MARE INTRE CEI 2 GEN+UNCHI")
    def verify_movement(self,main_body):
       pass