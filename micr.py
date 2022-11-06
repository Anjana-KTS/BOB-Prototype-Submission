#tesseract for micr detection using language 'mcr' from the trained model
import pytesseract as tess
from PIL import Image,ImageEnhance
import numpy as np
import cv2

# add tesseract to path
tess.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def micr(path):
    cheque_img = Image.open(path)

    #checking the mode
    cheque_img=np.array(cheque_img.convert('RGB'))

    shape=cheque_img.shape

    micr_extraction= cheque_img[int(shape[0]*0.92):int(shape[0]*0.99), int(shape[1]*0.25):int(shape[1]*0.8)]
    cv2.imwrite(r'micr.jpg',micr_extraction)
    micr_string=tess.image_to_string(micr_extraction,lang="mcr")
    # c000009c 60001205901 00274880 31
    # 0000000980 60001205901 00274880 31
    # c000009d0 60001205901 00274880 31
    # c000009c 60001205901 002748c 31
    # micr_string= "c000009c 60001205901 002748c 31"

    cheque_number=""
    '''The string before first space is cheque number'''
    val=micr_string.split()[0]
    if 'c' in micr_string:
        for i in val:
            if i.isdigit():
                cheque_number+=i
        
    else:
        ind=(len(val)-6)//2
        cheque_number=val[ind:ind+6]

    '''final micr'''
    final_micr=micr_string.split()[1][:9]
    Account_ID=micr_string.split()[2][:6]
    Transaction_code=micr_string[-3:]
    print(micr_string)
    print("Cheque number :",cheque_number)
    print("MICR code :",final_micr)
    print("Account ID :",Account_ID)
    print("Transaction code :",Transaction_code)
    return cheque_number,final_micr,Account_ID,Transaction_code


# print(micr(r'C:\Users\ANU\Downloads\bob_bhuvana_signNV_1.jpg'))