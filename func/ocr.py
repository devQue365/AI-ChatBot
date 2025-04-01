# Optical Code Recognition
# taking reference from - JaidedAI/EasyOCR
# ---- Requirements ----
# pip install easyocr -> to install Easy OCR
# pip install difflib -> to install difflib
# pip install pyautogui -> to install pyautogui
# pip install pil -> to install pillow (replacement of pil) (python imaging library)
# pip install opencv-python

import easyocr
import difflib
import pyautogui as pg# automate mouse movement
import cv2
import numpy as np
from PIL import ImageGrab # To take screenshot
from time import time as t

reader = easyocr.Reader(['en'], gpu=True)
# points ((x1,y1);(x2,y2)) -> 4 values
def center(points):
    # calculate the sum of x and y coordinates
    sum_x = sum(point[0] for point in points)
    sum_y = sum(point[1] for point in points)

    # calculate the center
    center_x = sum_x / len(points)
    center_y = sum_y / len(points)

    return int(center_x), int(center_y)



# Not optimized right now
def ocr_v1_clk(st, double_click=False):
    pg.sleep(0.5)  # Give time to UI to load
    screen = np.array(ImageGrab.grab())  # Take screenshot
    image_np = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    cv2.imwrite("debug_screenshot.png", cv2.cvtColor(screen, cv2.COLOR_RGB2BGR))
    c = t()
    result = reader.readtext(image_np)
    print(f"Read in {t()-c} seconds.")
    
    detected_texts = [i[1].lower() for i in result]
    # print("Detected Texts:", detected_texts)

    closest_match = difflib.get_close_matches(st, detected_texts, n=1, cutoff=0.3)
    # print("Closest Match:", closest_match)

    if closest_match:
        for i in result:
            if i[1].lower() == closest_match[0].lower():
                x, y = center(i[0])
                print(f"Clicking at: ({x}, {y})")
                
                screen_width, screen_height = pg.size()
                if 0 <= x < screen_width and 0 <= y < screen_height:
                    pg.sleep(0.2)
                    if double_click:
                        pg.click(x, y)
                        pg.sleep(0.5)
                        pg.click(x, y)
                    else:
                        pg.click(x, y)
                else:
                    print(f"Coordinates ({x}, {y}) are out of bounds!")
                    return f"Detected {st} but coordinates are invalid."
                
                return f"Clicked {closest_match[0]} sir."
    return f"No widget found named {st}."

