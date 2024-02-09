from skimage.metrics import structural_similarity as compare_ssim
import cv2

class CheckImageMatch():
    # def __repr__(self): #THIS CAN BE USED TO MAKE THE VALUE POSSIBLE TO BE CONVERTED TO ANOTHER TYPE WHEN IT IS RETURNED TO WHERE IT IS CALLED
    #     f"CheckImageMatch({self.score!r})"

    def __int__(self):
        return str(self.score)

    def __init__(self, imageA, imageB):
        self.imageA = imageA
        self.imageB = imageB
        # convert the images to grayscale
        self.grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        self.grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        (self.score, self.diff) = compare_ssim(self.grayA, self.grayB, full=True)
        self.diff = (self.diff * 255).astype("uint8")
