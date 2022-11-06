from PIL import Image,ImageEnhance
import cv2
import numpy as np

def processing(path):
    cheque_img = Image.open(path)

    #checking the mode
    cheque_img=cheque_img.convert('RGB')

    #contrast adjustments 

    enhancer = ImageEnhance.Contrast(cheque_img)
    factor = 2.5 #increase contrast
    cheque_img = enhancer.enhance(factor)

    #gray scale conversion
    cheque_img = cv2.cvtColor(np.array(cheque_img), cv2.COLOR_BGR2GRAY)

    #converting image float array into integer
    cheque_img = cheque_img / cheque_img.max() #normalizes data in range 0 - 255
    cheque_img = 255 * cheque_img
    cheque_img = cheque_img.astype(np.uint8)

    #converting image into black and white
    thresh=110
    cheque_img[cheque_img < thresh] = 0    # Black
    cheque_img[cheque_img >= thresh] = 255
    cv2.imwrite(path,cheque_img)


