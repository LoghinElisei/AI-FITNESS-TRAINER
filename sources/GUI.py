import cv2

org1 = (700, 200)
org2 = (50, 900)
orgCorrect = (1320, 200)
orgIncorrect = (1320, 300)
orgInfo1 = (20,200)
orgInfo2 = (20,300)
orgTitle = (850,85)
orgTitle2 = (720,85)
orgFeedback = (20,900)
orgAttention = (20,1000)
orgState = (20,600)
orgCommands = (1630,700)
font = cv2.FONT_HERSHEY_SIMPLEX
thickness = 3
fontScale = 2
text_format = "LOW CONFIDENCE Squats: 100 "
colorGreen = (0, 255, 0)
colorRed = (0,0,255)
colorWhite = (255,255,255)
colorYellow = (0,255,255)
colorTurquoise = (255,255,0)
colorBlack = (0,0,0)

SQUAT_STATE_MESSAGES = {
    "S0": "Standing",
    "S1": "Descending phase",
    "S2": "Bottom position"
}

def paint(frame, text, org, color, bg_color,font_scale = fontScale):

    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    x, y = org
    padding = 10

    cv2.rectangle(frame,
                  (x - padding, y - text_h - padding),
                  (x + text_w + padding, y + baseline ),
                  bg_color,
                  -1)


    cv2.putText(frame,
                text,
                org,
                font,
                font_scale,
                color,
                thickness)

def paint_rep_on_display(frame, val1, type_of_ex, color):

    text = f"{val1} {type_of_ex}"
    paint(frame, text, org1, color, (30, 30, 30))

def paint_on_display_background(frame, org):


    (text_w, text_h), baseline = cv2.getTextSize(text_format, font, fontScale, thickness)
    cv2.rectangle(frame,
                  (org[0] - 10, org[1] - text_h - 10),
                  (org[0] + text_w + 10, org[1] + baseline + 10),
                  (30, 30, 30),
                  -1)


def paint_text_on_display(frame, text, org):
    (text_w, text_h), baseline = cv2.getTextSize(text, font, fontScale, thickness)
    cv2.rectangle(frame,
                  (org[0] - 10, org[1] - text_h - 10),
                  (org[0] + text_w + 10, org[1] + baseline + 10),
                  (30, 30, 30),
                  -1)


def draw_command_menu(frame, start_pos):
    commands = [
        "Q - Quit",
        "P - Pause",
        "R - Reset",
        "1 - Squats",
        "2 - JJ",
        "3 - Push Ups"
    ]
    x, y = start_pos
    line_height = 60

    for cmd in commands:
        paint(frame,cmd,(x,y),colorWhite,colorBlack,font_scale=1)
        y += line_height