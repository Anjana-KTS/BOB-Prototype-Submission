from PIL import Image,ImageEnhance
import numpy as np
import cv2
def cropsign(path,signtuple):
    cheque_img = Image.open(path)
    cheque_img=np.array(cheque_img)
    
    x1,y1,x2,y2=signtuple
    sign = cheque_img[x1:y1,x2:y2]
    cv2.imwrite(r"sign.jpg",sign)

    
    image = Image.open(r"sign.jpg")
    rgb = image.convert('RGB')
    rgb.save(r'sign.png')
# 60001205901
# cropsign(r'page0.png',(308, 471, 1438, 1699))