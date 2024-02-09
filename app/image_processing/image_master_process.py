import cv2
import urllib.request, urllib.parse
import numpy as np
import pytesseract
from app.image_processing import enhance_image, draw_processed_image
from app.image_processing.image_processes import process_image_text_extended, process_image_text, process_image_only

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    

# async def fetch_image_result(image_no1, image_no2, is_object):
async def fetch_image_result(image_no1, image_no2):
    revert_process1= None
    revert_process2= None

    ingredients_common = []
    ingredients_difference= []



    # ++++++++++++++ ENCODING AN IMAGE STREAM URL +++++++++++++++++++++
    #  replacing spaces with %20 or using the urllib.parse.quote() function to automatically encode the URL components.
    image_no1_parse= urllib.parse.quote(image_no1[8:])
    image_path_restructure= "https://" + image_no1_parse

    image_no1 = urllib.request.urlopen(image_path_restructure)
    image_no1 = np.asarray(bytearray(image_no1.read()), dtype=np.uint8)
    image_no1 = cv2.imdecode(image_no1, cv2.IMREAD_COLOR)

    # +++++++++++++++ ENCODING A FILE IMAGE ++++++++++++++++++++

    image_no2= image_no2.read()
    image_no2 = np.frombuffer(image_no2, np.uint8)
    image_no2 = cv2.imdecode(image_no2, cv2.IMREAD_COLOR)


    check_match= process_image_only.CheckImageMatch(image_no1, image_no2).score * 100

    enhanced_image2= enhance_image.process(image_no2)
    im2= process_image_text.process(enhanced_image2)[12:].strip().replace('\n', '').split(',')
    if check_match >= 60:
        enhanced_image1= enhance_image.process(image_no1)
        # enhanced_image2= enhance_image.process(image_no2)

        im1= process_image_text.process(enhanced_image1)[12:].strip().replace('\n', '').split(',') #I AM SLICING OUT THE INGREDIENT NAME AT THE FRONT OF THE TEXT
        # im2= process_image_text.process(enhanced_image2)[12:].strip().replace('\n', '').split(',') #.strip() TO REMOVE LEADING AND TRAILING WHITESPACE

        ingredient_end_tracker1= im1[-1].split(' ')[-1]
        ingredient_end_tracker2 = im2[-1].split(' ')[-1]

        im1_extended= process_image_text_extended.process(enhanced_image1, ingredient_end_tracker1)
        im2_extended= process_image_text_extended.process(enhanced_image2, ingredient_end_tracker2)

        if im1_extended != [] and im2_extended != []:
            ingredients_common = list(set(im1_extended) & set(im2_extended))  # COMMON SET ITEMS, THEN CONVERTED BACK TO LIST
            ingredients_difference= list(set(im1_extended) ^ set(im2_extended)) #DIFFERENT SET ITEMS, THEN CONVERTED BACK TO LIST
                
            if len(ingredients_difference) != 0 or ingredients_difference != []:
                image_processed1= draw_processed_image.process(enhanced_image1, ingredient_end_tracker1, ingredients_difference)
                image_processed2= draw_processed_image.process(enhanced_image2, ingredient_end_tracker2, ingredients_difference)

                revert_process1= enhance_image.revers_and_convert(image_processed1)
                revert_process2= enhance_image.revers_and_convert(image_processed2)

        if ingredients_difference == ['']:
            ingredients_difference= []

        if ingredients_common == ['']:
            ingredients_common= []

        # print("INGRED1")
        # print(im1_extended)
        # print("INGRED2")
        # print(im2_extended)
        # print("\n\n")
        # print(ingredients_common)
        # print(ingredients_difference)
        
        if revert_process1 == None and revert_process2 == None:
            return {
                "detail": {"result": True, "common": ingredients_common, "difference": ingredients_difference, 'match_score': check_match},
                "new_ingredient": im2, "images": None
                }
        return {
            "detail": {"result": True, "common": ingredients_common, "difference": ingredients_difference, 'match_score': check_match},
            "new_ingredient": im2, "images": [revert_process1, revert_process2]
            }
    else:
        return {
            "detail": {"result": False, "common": None, "difference": None, 'match_score': check_match},  
            "new_ingredient": im2, "images": [None, None]
            }
        
        