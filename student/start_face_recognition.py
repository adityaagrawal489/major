import cv2
import numpy as np
import face_recognition
import os
import pickle
import getpass
from datetime import datetime

def start_face_recognition(userID,camera_type):
    getUser = getpass.getuser()
    ID = userID

    dat_name = "MODELS/" + str(ID) + ".dat"

    with open(dat_name, 'rb') as f:
        encodeListKnown = pickle.load(f)

    print("dat file loaded")
    cap = cv2.VideoCapture(camera_type)
    while True:
        ret, frame = cap.read()
        faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, ID, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
                #print(str(ID))
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) == 13:
            break
    