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

def select_image_by_id(conn, user_name):
    cur = conn.cursor()
    cur.execute("SELECT password, name, face_id FROM legal_people WHERE login_name=?", (user_name,))
    identification_data = cur.fetchall()
    return identification_data
 

database = "C:/GREENFOX/hackathon_fpush/database/authentication.db"
 
sql_create_table = """ CREATE TABLE IF NOT EXISTS legal_people (
                                row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                login_name TEXT NOT NULL,
                                password INT NOT NULL,
                                name TEXT NOT NULL,
                                user_or_admin TEXT NOT NULL,
                                face_id TEXT NOT NULL
                            ); """
  
user1 = ('Gyuri', random.randint(100000, 999999), 'Gyorgy Kardos', 'admin', 'C:/GREENFOX/megalotis-garnet/img/readme_imgs/gy_kardos.jpg')
user2 = ('Adam', random.randint(100000, 999999), 'Adam Kudar', 'admin', 'C:/GREENFOX/megalotis-garnet/img/readme_imgs/a_kudar.jpg')
user3 = ('Snocc', random.randint(100000, 999999), 'Istvan Schneider', 'admin', 'C:/GREENFOX/megalotis-garnet/img/readme_imgs/i_schneider.jpg')
user4 = ('Boro', random.randint(100000, 999999), 'Borbala Szakacs', 'admin','C:/GREENFOX/megalotis-garnet/img/readme_imgs/b_szakacs.jpg')
user5 = ('Zoli', random.randint(100000, 999999), 'Zoltan Egri', 'user', 'C:/GREENFOX/megalotis-garnet/img/readme_imgs/z_egri.jpg')
user6 = ('Benji', random.randint(100000, 999999), 'Gabor Bengyel', 'user', 'C:/GREENFOX/megalotis-garnet/img/readme_imgs/g_bengyel.jpg')
user7 = ('Peti', random.randint(100000, 999999), 'Peter Rozsnyai', 'user','C:/GREENFOX/megalotis-garnet/img/readme_imgs/p_rozsnyai.jpg')

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

