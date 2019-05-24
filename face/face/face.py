import numpy as np
import cv2 as cv
import imutils
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
    cur.execute("SELECT password, name, user_or_admin, face_id, finger_id FROM legal_people WHERE login_name=?", (user_name,))
    identification_data = cur.fetchall()
    return identification_data

def get_status_to_update(conn, user_name):
    cur = conn.cursor()
    cur.execute("SELECT user_or_admin FROM legal_people WHERE login_name =?", (user_name,))
    old_status = cur.fetchall()
    if old_status:
        if old_status[0][0] == 'admin':
            new_status = ('user', user_name)
            update_status(conn, new_status)
        else:
            new_status = ('admin', user_name)
            update_status(conn, new_status)
    else:
        print("Couldn't find user by given name")

def update_status(conn, new_status):
    sql = ''' UPDATE legal_people
             SET user_or_admin = ?
             WHERE login_name = ?'''
    cur = conn.cursor()
    cur.execute(sql, new_status)

def delete_user(conn, user_name):
    cur = conn.cursor()
    cur.execute("DELETE FROM legal_people WHERE login_name=?", (user_name,))
    has_succeeded = cur.fetchall()
    if has_succeeded:
        print("Operation done successfully")
    else:
        print("Couldn't find user by given name")

def download_database(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM legal_people")
    print(cur.fetchall())

def face_authentication():
    global username
    global password
    global full_name
    global status
    global image_id
    global finger_id
    
    passed = False

    database = "C:/database/authentication.db"

    while(True):
        username = input("Username:")
        password = getpass.getpass("Password:")
        conn = create_connection(database)
        with conn:
            user = select_image_by_id(conn, username)
        if user:
            if user[0][0] == int(password):
                break
        else:
            print("Username or password incorrect, please try again")
            continue

    full_name = user[0][1]
    status = user[0][2]
    image_id = user[0][3]

    loaded_image = face.load_image_file(image_id)
    user_face_to_find = [face.face_encodings(loaded_image)[0]]

    cap = cv.VideoCapture(0)

    face_locations = []
    face_encodings = []

    while(True):
        ret, frame = cap.read()
        rgb_frame = (frame[:, :, ::-1]).copy()
    
        frame = imutils.resize(frame, width=400)
        rgb_frame = imutils.resize(rgb_frame, width=400)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
        cv.imshow('frame', frame)

        face_locations = face.face_locations(rgb_frame)
        face_encodings = face.face_encodings(rgb_frame, face_locations)
    
        if face_locations:
            cv.rectangle(frame, (face_locations[0][3], face_locations[0][0]), (face_locations[0][1], face_locations[0][2]), (0, 0, 255), 2)
            cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    if face_encodings:
        match = face.compare_faces(user_face_to_find, face_encodings[0], tolerance = 0.50)
        if match[0]:
            print("Face authentication passed")
            passed = True
        else:
            print("Face does not match authorized person, you may try again")
    else:
        print("Couldn't detect any faces, please try again")

    cv.waitKey()
    cap.release()
    cv.destroyAllWindows()

    return passed

def fingerprint_authentication():
    cap = cv.VideoCapture(0)
    command = None

    while(True):
        ret, frame = cap.read()
        cv.imshow('frame', frame)

        if cv.waitKey(5) & 0xff == ord('q'):
                print("\nPress 'y' if you want to save the picture, else press any other key to take a new one.")
                command = input()

        if command == 'y':
            cv.imwrite("../../user_images/fingerprint.jpg", frame)
            user_photo = cv.imread("../../user_images/fingerprint.jpg", 1)
            break
        else:
            continue

def if_is_admin():
    command = None
    login_name = None
    full_name = None
    isUser = None
    user_photo = None

    database = "C:/database/authentication.db"

    while(True):
        print("\nWould you like to take any further actions? y/n")
        command = input()
        if command == 'n':
            print("Have a nice day!")
            break
        elif command == 'y':
            print("""\nPlease choose of the followings:

                'u' - create new user
                'a' - create new admin
                'm' - modify user/admin
                'r' - remove user/admin
                'p' - print database""")

        else:
            continue

        command = input()

        if command == 'u':
            login_name = input("\nEnter new user's login name:")
            full_name = input("Enter new user's full name:")
            status = 'user'

            cap = cv.VideoCapture(0)

            while(True):
                ret, frame = cap.read()
                cv.imshow('frame', frame)

                if cv.waitKey(5) & 0xff == ord('q'):
                    print("\nPress 'y' if you want to save the picture, else press any other key to take a new one.")
                    command = input()

                if command == 'y':
                    cv.imwrite("../../user_images/" + login_name + ".jpg", frame)
                    user_photo = cv.imread("../../user_images/" + login_name + ".jpg", 1)
                    break
                else:
                    continue
            new_user = (login_name, random.randint(100000, 999999), full_name, status, "../../user_images/" + login_name+".jpg")
            conn = create_connection(database)
            with conn:
                create_user(conn, new_user)
            print("New ID is registered with login_name: ", login_name, " name: ", full_name, " and status: ", status)
            cv.waitKey()

        elif command == 'a':
            login_name = input("\nEnter new user's login name:")
            full_name = input("Enter new user's full name:")
            status = 'admin'

            cap = cv.VideoCapture(0)

            while(True):
                ret, frame = cap.read()
                cv.imshow('frame', frame)

                if cv.waitKey(5) & 0xff == ord('q'):
                    print("\nPress 'y' if you want to save the picture, else press any other key to take a new one.")
                    command = input()

                if command == 'y':
                    cv.imwrite("../../user_images/" + login_name + ".jpg", frame)
                    user_photo = cv.imread("../../user_images/" + login_name + ".jpg", 1)
                    break
                else:
                    continue

            new_user = (login_name, random.randint(100000, 999999), full_name, status, "../../user_images/" + login_name + ".jpg")
            conn = create_connection(database)
            with conn:
                create_user(conn, new_user)
            print("New ID is registered with login_name: ", login_name, " name: ", full_name, " and status: ", status)
            cv.waitKey()

        elif command == 'm':
            login_name = input("\nEnter the user's login_name, who you want to modify:")
            conn = create_connection(database)
            with conn:
                get_status_to_update(conn, login_name)

        elif command == 'r':
            login_name = input("\nEnter the user's login_name, who you want to remove:")
            conn = create_connection(database)
            with conn:
                delete_user(conn, login_name)

        elif command == 'p':
            conn = create_connection(database)
            with conn:
                download_database(conn)

        else:
            continue

    else:
        print("Have a nice day!")


username = None
password = None
full_name = None
status = None
image_id = None
finger_id = None

is_authorized = face_authentication()

if is_authorized:
    fingerprint_authentication()

if status == 'admin':
    if_is_admin()
else:
    print("Have a nice day!")