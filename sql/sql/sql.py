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
    sql = ''' INSERT INTO legal_people(login_name,password,name,user_or_admin,face_id)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

database = "C:/database/authentication.db"
 
sql_create_table = """ CREATE TABLE IF NOT EXISTS legal_people (
                                row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                login_name TEXT NOT NULL,
                                password INT NOT NULL,
                                name TEXT NOT NULL,
                                user_or_admin TEXT NOT NULL,
                                face_id TEXT NOT NULL
                            ); """
  
user1 = ('Gyuri', random.randint(100000, 999999), 'Gyorgy Kardos', 'admin', '../../user_images/gy_kardos.jpg')
user2 = ('Adam', random.randint(100000, 999999), 'Adam Kudar', 'admin', '../../user_images/a_kudar.jpg')
user3 = ('Snocc', random.randint(100000, 999999), 'Istvan Schneider', 'admin', '../../user_images/i_schneider.jpg')
user4 = ('Boro', random.randint(100000, 999999), 'Borbala Szakacs', 'admin','../../user_images/b_szakacs.jpg')
user5 = ('Zoli', random.randint(100000, 999999), 'Zoltan Egri', 'user', '../../user_images/z_egri.jpg')
user6 = ('Benji', random.randint(100000, 999999), 'Gabor Bengyel', 'user', '../../user_images/g_bengyel.jpg')
user7 = ('Peti', random.randint(100000, 999999), 'Peter Rozsnyai', 'user','../../user_images/p_rozsnyai.jpg')

conn = create_connection(database)
if conn is not None:
    create_table(conn, sql_create_table)
else:
    print("Error! cannot create the database connection.")
with conn:
    create_user(conn, user1)
    create_user(conn, user2)
    create_user(conn, user3)
    create_user(conn, user4)
    create_user(conn, user5)
    create_user(conn, user6)
    create_user(conn, user7)

