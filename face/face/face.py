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

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_user(conn, user):
    sql = ''' INSERT INTO legal_people(login_name,password,name,face_id)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

def select_image_by_id(conn, user_name):
    cur = conn.cursor()
    cur.execute("SELECT password, name, face_id FROM legal_people WHERE login_name=?", (user_name,))
    identification_data = cur.fetchall()
    return identification_data
 

database = "C:/GREENFOX/gfa_hack_fpush/database/authentication.db"
 
sql_create_table = """ CREATE TABLE IF NOT EXISTS legal_people (
                                row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                login_name TEXT NOT NULL,
                                password INT NOT NULL,
                                name TEXT NOT NULL,
                                face_id TEXT NOT NULL
                            ); """
  
user1 = ('Gyuri', random.randint(100000, 999999), 'Gyorgy Kardos', 'C:/GREENFOX/megalotis-garnet/img/readme_imgs/gy_kardos.jpg')
user2 = ('Adam', random.randint(100000, 999999), 'Adam Kudar', 'C:/GREENFOX/megalotis-garnet/img/readme_imgs/a_kudar.jpg')
user3 = ('Snocc', random.randint(100000, 999999), 'Istvan Schneider', 'C:/GREENFOX/megalotis-garnet/img/readme_imgs/i_schneider.jpg')
user4 = ('Boro', random.randint(100000, 999999), 'Borbala Szakacs', 'C:/GREENFOX/megalotis-garnet/img/readme_imgs/b_szakacs.jpg')

conn = create_connection(database)
if conn is not None:
    create_table(conn, sql_create_table)
else:
    print("Error! cannot create the database connection.")

#conn = create_connection(database)
#with conn:
    #create_user(conn, user1)
    #create_user(conn, user2)
    #create_user(conn, user3)
    #create_user(conn, user4)

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
    print("Face autenthication passed")
else:
    print("Face does not match authorized person")

cap.release()
cv.destroyAllWindows()
