from GUI import *
from jumping_jacks_angles import *
from sources.verify import play_beep_async


class JumpingJacks:
    def __init__(self):
        self.state = "S0"
        self.arm_angle_avg = 0
        self.legs_angle = 0
        self.message = "Start Jumping"
        self.correct = 0
        self.last_state = "S0"

    def paint(self, image_left_ocv, main_body):
        if verify_confidence(main_body):
            paint_on_display_background(image_left_ocv, org1)

            info_text = f"Arms: {int(self.arm_angle_avg)} | Legs: {int(self.legs_angle)}"
            paint_rep_on_display(image_left_ocv, info_text, "Jumping Jacks", (255, 165, 0))

            paint(image_left_ocv, f"COUNT : {self.correct} ", org3, color=(255, 255, 255), background_color=(0, 255, 0))

            status_text = "OPEN" if self.state == "S1" else "CLOSE"
            paint(image_left_ocv, f"State: {status_text}", org6, color=(0, 255, 255), background_color=(0, 0, 0))

        else:
            paint_on_display_background(image_left_ocv, org1)
            paint_rep_on_display(image_left_ocv, "LOW CONFIDENCE", "Jumping Jacks", (0, 0, 255))

        if self.message != "":
            paint(image_left_ocv, self.message, org5, color=(255, 255, 255), background_color=(0, 0, 255))

    def detect(self, main_body):
        if verify_confidence(main_body):
            left_arm, right_arm = compute_arm_angles(main_body)
            self.legs_angle = compute_legs_angle(main_body)

            self.arm_angle_avg = (left_arm + right_arm) / 2

            if self.state == "S0":
                if self.arm_angle_avg > 100 and self.legs_angle > 30:
                    self.state = "S1"
                    self.message = "Good Jump!"
                    play_beep_async()

            elif self.state == "S1":
                if self.arm_angle_avg < 45 and self.legs_angle < 25:
                    self.state = "S0"
                    self.correct += 1
                    self.message = "Down"