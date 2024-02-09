import io

import cv2
import numpy as np
from fastapi.responses import StreamingResponse


def process(img1):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    #++++++++++++++++++++ SHARPENING IMAGE +++++++++++++++++++++++++++++
    blurred = cv2.GaussianBlur(gray1, (5, 5), 0)
    # Define the sharpening kernel
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    # Apply the kernel using filter2D function
    sharpened = cv2.filter2D(blurred, -1, kernel)
    #+++++++++++++++++++    SHARPENING IMAGE ENDS ++++++++++++++++++++++++++
    return sharpened



def revers_and_convert(img1):
    #++++++++++++++++++++ REVERSING IMAGE COLOR TO COLORED ++++++++++++
    colored = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    #++++++++++++++++++++ BLURRING IMAGE +++++++++++++++++++++++++++++
    # blurred = cv2.GaussianBlur(colored, (5, 5), 0)
    # cv2.imshow('blurred', blurred)
    # cv2.waitKey(0)

    # +++++++ CONVERTING BACK TO BINARY BUFFERS AND STREAMING RESPONSE
    _, buffer = cv2.imencode('.jpg', colored)
    stream_response= StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")
    return stream_response

