import sqlite3


def seed_users():
    users = [
        {"username": 'admin', "password": 'qweasdzxc'},
        {"username": 'John', "password": '07RYbe$!9y11'},
        {"username": 'Jane', "password": '07RYbe$!9y12'},
    ]

    con = sqlite3.connect("db.db")
    cur = con.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, username, password)
                ''')
    cur.executemany(
        'INSERT INTO users(username, password) VALUES (:username, :password)', users)

    # print all users from sqlite
    for row in cur.execute("SELECT id, username, password FROM users"):
        print(row)

    con.commit()
    con.close()


def get_user(username, password):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password,))
    user = cur.fetchone()
    con.close()
    if not user:
        return None
    return {"id": user[0], "username": user[1]}


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
        "SELECT username FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    if not user:
        return None
    return {"name": user[0]}


def get_user_by_id(id):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(
        "SELECT id, username FROM users WHERE id = ?", (id,))
    user = cur.fetchone()
    con.close()
    return {"id": user[0], "username": user[1]}


def create_user(username, password):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users(username, password) VALUES (?,?)", (username, password))
    con.commit()
    con.close()
