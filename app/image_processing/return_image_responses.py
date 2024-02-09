import io

from  fastapi.responses import JSONResponse, StreamingResponse
import cv2
import numpy as np


def generate_return(json_body, img1, img2):
    if (img1 != None and img2 != None):
        # Convert the processed images to binary buffers
        _, buffer1 = cv2.imencode('.jpg', img1)
        _, buffer2 = cv2.imencode('.jpg', img2)

        buffer1= io.BytesIO(buffer1.tobytes())
        buffer2 = io.BytesIO(buffer2.tobytes())

        json_body= json_body

        JSON_RESPONSE= JSONResponse(content= json_body, status_code= 201, media_type= "application/json")
        FILE_STREAM_RESPONSE1= StreamingResponse(buffer1, media_type= "image/jpeg")
        FILE_STREAM_RESPONSE2 = StreamingResponse(buffer2, media_type="image/jpeg")

    else:
        JSON_RESPONSE = JSONResponse(content=json_body, status_code=201, media_type="application/json")
        FILE_STREAM_RESPONSE1 = img1
        FILE_STREAM_RESPONSE2 = img2
    return (JSON_RESPONSE, FILE_STREAM_RESPONSE1, FILE_STREAM_RESPONSE2)