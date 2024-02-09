import re

import cv2
import pytesseract
import numpy as np
from pytesseract import Output


def process(sharpened, ingredient_end_tracker):
    ingredient_tracker = False

    #++++++++++++++ DRAWING TEXTS ON SCREEN +++++++++++++++++++
    add_texts= []


    boxes = (pytesseract.image_to_data(sharpened))
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])

                getTxt = str(b[11]).upper()

                if getTxt == "INGREDIENTS:" or getTxt== "INGREDIENTS" or ingredient_tracker:
                    ingredient_tracker = True
                    add_texts.append(getTxt)

                    if getTxt== ingredient_end_tracker:
                        break

    return add_texts
