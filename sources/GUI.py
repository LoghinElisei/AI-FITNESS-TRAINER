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


def paint_rep_on_display(frame, val1, type_of_ex, color):

    text = f"{val1} {type_of_ex}"
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
