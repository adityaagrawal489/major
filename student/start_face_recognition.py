import cv2
import numpy as np
import face_recognition
import os
import pickle
import getpass
from datetime import datetime
import time
from datetime import datetime
 
def time_diff(start,end):
    start_dt = datetime.strptime(start, '%H:%M:%S')
    end_dt = datetime.strptime(end, '%H:%M:%S')
    diff = (end_dt - start_dt) 
    return(diff.seconds/60) 

starttime = time.time()
def start_face_recognition(userID,camera_type,start_time,end_time):
    getUser = getpass.getuser()
    ID = userID

    dat_name = "MODELS/" + str(ID) + ".dat"

    with open(dat_name, 'rb') as f:
        encodeListKnown = pickle.load(f)

    print("dat file loaded")
    cap = cv2.VideoCapture(camera_type)
    count=0
    print(time_diff(start_time,end_time))
    min_count=time_diff(start_time,end_time)
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
                count+=1
                print(str(ID))
        # cv2.imshow('Webcam', frame)
        currentDateAndTime = datetime.now()
        print("The current date and time is", currentDateAndTime)
        currentTime = currentDateAndTime.strftime("%H:%M:%S")
        # end_dt = datetime.strptime(end_time, "%H:%M:%S")
        
        print(currentTime)
        print(end_time)
        if(currentTime>=(end_time)):
            print(count)
            if (count/min_count)>0.50:
                return True
            else:
                return False
        if cv2.waitKey(1) == 13:
            break
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))