import numpy as np
import cv2 as cv
import face_recognition as face
import sqlite3, random, getpass
from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def create_user(conn, user):
    sql = ''' INSERT INTO legal_people(login_name,password,name,user_or_admin,face_id)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

def select_image_by_id(conn, user_name):
    cur = conn.cursor()
    cur.execute("SELECT password, name, face_id FROM legal_people WHERE login_name=?", (user_name,))
    identification_data = cur.fetchall()
    return identification_data

def download_database(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM legal_people")
    print(cur.fetchall())

database = "C:/GREENFOX/hackathon_fpush/database/authentication.db"
 
username = None
password = None
sqlUsername = None
sqlPassword = None

while(True):
    username = input("Username:")
    password = getpass.getpass("Password:")
    conn = create_connection(database)
    with conn:
        user = select_image_by_id(conn, username)
    if user[0][0] == int(password):
        break

user_full_name = user[0][1]
user_image = user[0][2]

image = face.load_image_file(user_image)
user_face_to_find = [face.face_encodings(image)[0]]

cap = cv.VideoCapture(0)

face_locations = []
face_encodings = []
face_names = []

while(True):
    ret, frame = cap.read()
    rgb_frame = (frame[:, :, ::-1]).copy()
    cv.imshow('frame', frame)
    face_locations = face.face_locations(rgb_frame)
    face_encodings = face.face_encodings(rgb_frame, face_locations)
    if face_locations:
        cv.rectangle(frame, (face_locations[0][3], face_locations[0][0]), (face_locations[0][1], face_locations[0][2]), (0, 0, 255), 2)
        cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

match = face.compare_faces(user_face_to_find, face_encodings[0], tolerance = 0.50)

if match[0]:
    print("Face authentication passed")
else:
    print("Face does not match authorized person")

conn = create_connection(database)
download_database(conn)
 
cv.waitKey()
cap.release()
cv.destroyAllWindows()
