import re

import cv2
import pytesseract
import numpy as np
from pytesseract import Output

save_as_filename= 0
def process(sharpened, ingredient_end_tracker, disparities_list):
    global  save_as_filename
    save_as_filename+= 1
    #++++++++++++++ DRAWING WORDS ON SCREEN +++++++++++++++++++
    boxes = (pytesseract.image_to_data(sharpened))
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])

                getTxt = str(b[11]).upper()

                if getTxt in disparities_list:
                    # add_texts.append(getTxt)
                    cv2.rectangle(sharpened, (x, y), (w + x, h + y), (0, 0, 255), 2)

                    if getTxt== ingredient_end_tracker:
                        break

                # cv2.putText(sharpened, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)

    cv2.imwrite(f'image_results/{save_as_filename}.jpg', sharpened)
    # cv2.imshow('sharpened', sharpened)
    # cv2.waitKey(0)
    return  sharpened

