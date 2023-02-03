import sqlite3


def generate_username(name, lastname):
    username = name[0] + lastname + "-"
    username = username.lower()

    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(
        "SELECT COUNT(username) FROM users WHERE username LIKE ?", (username + "%",))
    count = cur.fetchone()
    con.close()
    return username + str(count[0])


def seed_users():
    # name, lastname, username, password, email, phone
    users = [
        {"name": 'John', "lastname": "Doe", "password": '07RYbe$!9y11',
            "address": "1234 Main St", "phone": "123-456-7890"},
        {"name": 'Frederick', "lastname": "Mccarthy", "password": '07RYbe$!9y12',
            "address": "1234 Main St", "phone": "123-456-7890"},
        {"name": 'Angelica', "lastname": "Lu", "password": '07RYbe$!9y13',
            "address": "1234 Main St", "phone": "123-456-7890"},
        {"name": 'Emile', "lastname": "Wright", "password": '07RYbe$!9y14',
            "address": "1234 Main St", "phone": "123-456-7890"},
        {"name": 'Amarah', "lastname": "Bruce", "password": '07RYbe$!9y15',
            "address": "1234 Main St", "phone": "123-456-7890"},
    ]

    # generate username and email from name and lastname
    for user in users:
        username = user["name"][0] + user["lastname"] + "-" + "0"
        user["username"] = username.lower()
        email = user["name"] + "@" + user["lastname"] + ".com"
        user["email"] = email.lower()

    con = sqlite3.connect("db.db")
    cur = con.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, name, lastname, username, password, address, phone, email)
                ''')
    cur.executemany(
        'INSERT INTO users(name, lastname, username, password, address, phone, email) VALUES (:name, :lastname, :username, :password, :address, :phone, :email)', users)

    # print all users from sqlite
    for row in cur.execute("SELECT id, name, lastname, username, password, address, phone, email FROM users"):
        print(row)

    con.commit()
    con.close()


def get_user(email, password):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(
        "SELECT id, username, password FROM users WHERE email = ? AND password = ?", (email, password))
    user = cur.fetchone()
    con.close()
    if not user:
        return None
    return {"id": user[0], "username": user[1], "password": user[2]}


def get_all_user():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(
        "SELECT name, lastname FROM users")
    users = cur.fetchall()
    con.close()
    users_list = [{"name": user[0], "lastname": user[1]} for user in users]
    return users_list


def get_user_by_username(username):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(
        "SELECT name, lastname, username, address, phone, email FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    if not user:
        return None
    return {"name": user[0], "lastname": user[1], "username": user[2], "address": user[3], "phone": user[4], "email": user[5]}


def get_user_by_id(id):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(
        "SELECT id, name, lastname, username, address, phone, email FROM users WHERE id = ?", (id,))
    user = cur.fetchone()
    con.close()
    return {"id": user[0], "name": user[1], "lastname": user[2], "username": user[3], "address": user[4], "phone": user[5], "email": user[6]}


def create_user(name, lastname, username, password, address, phone, email):
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    cur.execute("INSERT INTO users(name, lastname, username, password, address, phone, email) VALUES (?,?,?,?,?,?,?)",
                (name, lastname, username, password, address, phone, email))

    con.commit()
    con.close()


def check_email(email):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT email FROM users WHERE email = ?", (email,))
    email = cur.fetchone()
    con.close()
    return email
