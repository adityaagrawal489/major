import cv2
import numpy as np
import face_recognition
import os
import pickle
import sys
import time
import getpass
from . import delete_folder
from PIL import Image
from datetime import datetime

def train_model(ID):    
    parent = "C:/Users/Dell/Desktop/FROM SCRATCH/FRESH START 2/"
    folder_loc = ID+"/"
    images = []
    personNames = []
    myList = os.listdir(folder_loc)
    for cu_img in myList:
        current_Img = cv2.imread(f'{folder_loc}/{cu_img}')
        images.append(current_Img)
        personNames.append(os.path.splitext(cu_img)[0])
    
    current_time = datetime.now().strftime("%H:%M:%S")
    print("Current Time =", current_time)

    encodeList = []

    op = faceEncodings(images,encodeList)

    print("RESULT + " + str(op))

    if(op==0):
        print("INVALID FACE")
        return

    dat_name = "MODELS/" + str(ID) + ".dat"

    with open(dat_name, 'wb') as f:
        pickle.dump(encodeList, f)

    print("DELETING PHOTOS")

    #delete_folder.delete_folder(folder_loc)

    time.sleep(1)

    print("PHOTOS DELETED")

    current_time = datetime.now().strftime("%H:%M:%S")
    print("Current Time =", current_time)

def faceEncodings(imgList,encodeList):
    
    i = 0
    for img in imgList:
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except Exception as inst:
            print(str(inst))
        i += 1
    
    if(len(encodeList)==0):
        return 0

    return 1

