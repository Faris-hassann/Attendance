import datetime
import cv2
import cmake
import dlib
import face_recognition
import numpy as np
import os
import pandas as pd
import openpyxl
import xlsxwriter
import csv

#create a new excel sheet
now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y_%m_%d')
path = 'D:/python/images/'

#list for the images to put inside
images = []

#list for the names
classnames = []

# put the images in the list
my_list = os.listdir(path)
print(my_list)

#append the last word from the list
for cl in my_list:
    current_image = cv2.imread(f'{path}/{cl}')
    images.append(current_image)
    classnames.append(os.path.splitext(cl)[0])

# print the names in the class
print(classnames)

# find encoding functions
def find_encoding(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list

def compare():
    with open('attendance.csv', 'r') as t1, open('TT_list.csv', 'r') as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

    with open(now_time + '.csv', 'w') as outFile:
        for line in fileone:
            if line not in filetwo:
                outFile.write(line)


def mark_the_attendance(name):
    with open('attendance.csv', 'r+') as f:
        my_data_list = f.readlines()
        name_list = []
        for line in my_data_list:
            entry = line.split(',')
            name_list.append(entry[0])
        if name not in name_list:
            now = datetime.datetime.now()
            dtstring = now.strftime('%H:%M')
            f.writelines(f'\n{name}, {dtstring}')
        
#known images
print("Encoding...")
encode_list_known = find_encoding(images)
print("encoding is complete...")

#open camera
cap = cv2.VideoCapture(1)
while True:
    success, img = cap.read()
    image_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    image_small = cv2.cvtColor(image_small, cv2.COLOR_BGR2RGB)

    #find the location of the face
    face_current_frame = face_recognition.face_locations(image_small)
    encodes_current_frame = face_recognition.face_encodings(image_small, face_current_frame)

    #compare the faces in the program with the videos
    for encode_face, face_location in zip(encodes_current_frame, face_current_frame):
        matches = face_recognition.compare_faces(encode_list_known, encode_face)
        face_distance = face_recognition.face_distance(encode_list_known, encode_face)
        match_index = np.argmin(face_distance)

        if matches[match_index]:
            name = classnames[match_index].upper()
            print(name)
            y1, y2, x1, x2 = face_location
            y1, y2, x1, x2 = y1*4, y2*4, x1*4, x2*4
            mark_the_attendance(name)
            #cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            #cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            #cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255,255), 2)

    cv2.imshow('TEST', img)
    cv2.waitKey(1)
    compare()