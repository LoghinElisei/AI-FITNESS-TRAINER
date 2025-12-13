from GUI import *
from jumping_jacks_angles import *
from sources.verify import play_beep_async


class JumpingJacks:
    def __init__(self):
        self.state = "S0"
        self.arm_angle = 0
        self.legs_angle = 0
        self.message = "Start Jumping"
        self.message_template = [colorRed,colorWhite]
        self.message_state = "STANDING"
        self.correct = 0
        self.incorrect = 0
        self.last_state = "S0"

    def paint(self, image_left_ocv, main_body):
        paint(image_left_ocv, "JUMPING JACKS", orgTitle2, color=(252, 34, 0), bg_color=(14, 201, 255))
        draw_command_menu(image_left_ocv, orgCommands)
        paint(image_left_ocv, f"CORRECT : {self.correct}  ", orgCorrect, color=(255, 255, 255), bg_color=(0, 255, 0))
        paint(image_left_ocv, f"INCORRECT : {self.incorrect}", orgIncorrect, color=(255, 255, 255),
              bg_color=(0, 0, 255))
        paint(image_left_ocv, f"Arm Angle: {int(self.arm_angle)}", orgInfo1, color=(0, 255, 0), bg_color=(0, 0, 0))
        paint(image_left_ocv, f"Legs Angle: {int(self.legs_angle)}", orgInfo2, color=(0, 255, 0), bg_color=(0, 0, 0))
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
            left_arm, right_arm = compute_arm_angles(main_body)
            self.legs_angle = compute_legs_angle(main_body)

            self.arm_angle = (left_arm + right_arm) / 2

            if self.state == "S0":
                self.message_state = "CLOSE"
                if self.arm_angle > 100 and self.legs_angle > 30:
                    self.state = "S1"
                    self.message = "Good Jump!"
                    self.message_template = [colorYellow, colorBlack]
                    self.last_state = "S0"
                    play_beep_async()

            elif self.state == "S1":
                self.message_state="OPEN"
                if self.arm_angle < 45 and self.legs_angle < 25:
                    self.state = "S0"
                    self.last_state = "S1"
                    self.correct += 1
                    self.message = "Good Job"
                    self.message_template = [colorGreen, colorWhite]