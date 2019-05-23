import numpy as np
import cv2 as cv
import face_recognition as face

cap = cv.VideoCapture(0)

female_image = face.load_image_file("C:/GREENFOX/megalotis-garnet/img/readme_imgs/b_szakacs.jpg")
female_face_encoding = face.face_encodings(female_image)[0]

male_image = face.load_image_file("C:/GREENFOX/megalotis-garnet/img/readme_imgs/a_kudar.jpg")
male_face_encoding = face.face_encodings(male_image)[0]

male1_image = face.load_image_file("C:/GREENFOX/megalotis-garnet/img/readme_imgs/gy_kardos.jpg")
male1_face_encoding = face.face_encodings(male1_image)[0]

male2_image = face.load_image_file("C:/GREENFOX/megalotis-garnet/img/readme_imgs/i_schneider.jpg")
male2_face_encoding = face.face_encodings(male2_image)[0]

known_faces = [
    female_face_encoding,
    male_face_encoding,
    male1_face_encoding,
    male2_face_encoding
    ]

face_locations = []
face_encodings = []
face_names = []
frame_number = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    frame_number = 1
    rgb_frame = (frame[:, :, ::-1]).copy()

    # Display the resulting frame
    #cv.imshow('frame', frame)
    face_locations = face.face_locations(rgb_frame)
    face_encodings = face.face_encodings(rgb_frame, face_locations)
    if face_locations:
        cv.rectangle(frame, (face_locations[0][3], face_locations[0][0]), (face_locations[0][1], face_locations[0][2]), (0, 0, 255), 2)
        cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

face_names = []
name = None
for face_encoding in face_encodings:
    match = face.compare_faces(known_faces, face_encoding, tolerance = 0.50)
    if match[0]:
        name = "Borika"
        print("ez a Borika")
    elif match[1]:
        name = "Adika"
        print("ez az AAdika")
    elif match[2]:
        name = "Gyurika"
        print("ez a Gyurika")
    elif match[3]:
        name = "Pista"
        print("ez a Pista")
    else:
        print("ez nem is az AAdika nem is a Borika nem is a Gyurika nem is a Pista")

face_names.append(name)

for (top, right, bottom, left), name in zip(face_locations, face_names):
    if not name:
        continue
    cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
