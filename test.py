from typing import runtime_checkable

import cv2
import pyzed.sl as sl


def draw_line (frame, first, end):
    # if (kp_a[0] < left_display.shape[1] and kp_a[1] < left_display.shape[0]
    #         and kp_b[0] < left_display.shape[1] and kp_b[1] < left_display.shape[0]

    if (first[0] > 0 and first[1] > 0 and end[0] > 0 and end[1] > 0
            and first[0] < frame.shape[1] and first[1] < frame.shape[0]
            and end[0] < frame.shape[1] and end[1] < frame.shape[0]):
        cv2.line(frame, first, end, (0, 255, 0,), 2, cv2.LINE_AA)

def draw_skeleton (frame, body_parts):
    # neck
    # cv2.line(frame, body_parts[0], body_parts[1],(0, 255, 0,), 2)

    # left arm
    draw_line(frame, body_parts[1], body_parts[2])
    draw_line(frame, body_parts[2], body_parts[3])
    draw_line(frame, body_parts[3], body_parts[4])

    # right arm
    draw_line(frame, body_parts[1], body_parts[5])
    draw_line(frame, body_parts[5], body_parts[6])
    draw_line(frame, body_parts[6], body_parts[7])

    # body
    draw_line(frame, body_parts[2], body_parts[8])
    draw_line(frame, body_parts[5], body_parts[11])
    draw_line(frame, body_parts[8], body_parts[11])

    # leftleg
    draw_line(frame, body_parts[8], body_parts[9])
    draw_line(frame, body_parts[9], body_parts[10])

    # rightleg
    draw_line(frame, body_parts[11], body_parts[12])
    draw_line(frame, body_parts[12], body_parts[13])

zed = sl.Camera()

# Parametri de inițializare
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD720
init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
init_params.coordinate_units = sl.UNIT.METER

# Deschide camera
err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    print("Eroare la deschiderea camerei:", err)
    exit(1)


tracking_params = sl.PositionalTrackingParameters()
err = zed.enable_positional_tracking(tracking_params)
if err != sl.ERROR_CODE.SUCCESS:
    print("Eroare la positional tracking:", err)
    zed.close()
    exit(1)


body_params = sl.BodyTrackingParameters()
body_params.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_FAST
body_params.enable_tracking = True
body_params.enable_body_fitting = True
body_params.body_format = sl.BODY_FORMAT.BODY_18

err = zed.enable_body_tracking(body_params)
if err != sl.ERROR_CODE.SUCCESS:
    print("Eroare la activarea body tracking:", err)
    zed.close()
    exit(1)

runtime_params = sl.RuntimeParameters()

body_runtime_param = sl.BodyTrackingRuntimeParameters()
body_runtime_param.detection_confidence_threshold = 40

bodies = sl.Bodies()
image = sl.Mat()

while True:
    if zed.grab(runtime_params) == sl.ERROR_CODE.SUCCESS:
        zed.retrieve_image(image, sl.VIEW.LEFT)
        frame = image.get_data()
        zed.retrieve_bodies(bodies, body_runtime_param)
        if bodies.body_list:
            body = bodies.body_list[0] #avem doar o persoana
            body_parts = []


            for body_part in body.keypoint_2d:
                x = body_part[0]
                y = body_part[1]
                body_parts.append((int(x), int(y)))
                if x > 0 and y > 0:
                    cv2.circle(frame, (int(x),int(y)), 5, (0, 255, 0,), -1)

            # print (body_parts)

            draw_skeleton(frame, body_parts)


            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(frame, 'OpenCV', (10, 500), font, 4, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Zed2i - live", frame)

        if cv2.waitKey(1) == 27:  # ESC
            break

cv2.destroyAllWindows()
zed.close()

print ("inchidere camera")
