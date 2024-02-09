import re

import cv2
import pytesseract
import numpy as np
from pytesseract import Output


def process(sharpened):
    ingredient_tracker = ''
    save_ingredient = ''
    no = 0


    text_return= pytesseract.image_to_string(sharpened)
    text_return = text_return.replace(text_return[len(text_return) - 1], '')

    #+++++++++++++++ EXTRACTING THE INGREDIENTS ++++++++++++++++++
    for i in text_return:
        if ingredient_tracker == "ingredient":
            try:
                if i != '\n' or text_return[no - 1] != '\n' or text_return[no - 2] == ',': #IN CASE OF ANY UNUSUAL RESULT, THIS PLACE NEEDS TO BE REMEMBERED, THE LAST CONDITIONAL STATEMENT OF ',' MAY BE REMOVED
                    save_ingredient += i.upper()
                else:
                    break
            except:
                pass
        if i.lower() == 'i':
            try:
                token = i + text_return[no + 1] + text_return[no + 2] + text_return[no + 3] \
                        + text_return[no + 4] + text_return[no + 5] + text_return[no + 6] \
                        + text_return[no + 7] + text_return[no + 8] + text_return[no + 9]
                if ingredient_tracker != "ingredient":
                    if token.lower() == "ingredient":
                        ingredient_tracker = token.lower()
                        save_ingredient += 'I'

            except:
                pass
        no += 1
    return save_ingredient





