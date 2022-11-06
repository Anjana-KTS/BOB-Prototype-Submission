# pip install pdf2image
# pip install fpdf
#  pip install PyPDF2

# import module
from pdf2image import convert_from_path
from PIL import Image,ImageEnhance
import numpy as np
import cv2

import os
from PyPDF2 import PdfWriter, PdfReader
import requests
import json
import time
from requests import get, post


def pdf(path):
    # Store Pdf with convert_from_path function
    images = convert_from_path(path,poppler_path = r"C:\Program Files\poppler-0.68.0\bin")
    
    for i in range(0,len(images)):
        # Save pages as images in the pdf
        path = 'static/uploads/Chequeimages/page'+ str(i) +'.png'
        images[i].save(path, 'PNG')

    print("Processed images")

