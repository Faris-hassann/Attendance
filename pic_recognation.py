import cmake
import dlib
import face_recognition
import numpy as np
import cv2

#functions
def write_in_File():
    file_Write = open("attend.txt", "a")
    if(file_Write != True):
        print("something went wrong")
    else:
        file_Write.write("Name: Faris Hassan  ID: 11")
        file_Write.close()

#open faris main picture
Faris = face_recognition.load_image_file('D:/python/images/faris.jpeg')
Faris = cv2.cvtColor(Faris, cv2.COLOR_BGR2RGB)

#open the test image
imgTest = face_recognition.load_image_file('D:/python/images/seleem.jpeg')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

#find the location of the face in faris image
Faris_location = face_recognition.face_locations(Faris)[0]
Faris_encoding = face_recognition.face_encodings(Faris)[0]
cv2.rectangle(Faris,(Faris_location[3],Faris_location[0]),(Faris_location[1],Faris_location[2]), (255, 0, 255),2)

#find the location of the face in faris test image
Faris_location_test = face_recognition.face_locations(imgTest)[0]
Faris_encoding_test = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest,(Faris_location_test[3], Faris_location_test[0]), (Faris_location_test[1], Faris_location_test[2]), (255, 0, 255), 2)

results = face_recognition.compare_faces([Faris_encoding], Faris_encoding_test)
print(results)

if (results == True):
    write_in_File()

cv2.imshow('Faris Hassan', Faris)
cv2.imshow('image test', imgTest)
cv2.waitKey(0)