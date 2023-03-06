import sqlite3


def seed_users():
    users = [('Michael', '07RYbe$!9y11'),
             ('Adam', '07RYbe$!9y12'),
             ('Andrew', '07RYbe$!9y13'),
             ]

    con = sqlite3.connect("db.db")
    cur = con.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, username, password)
                ''')
    cur.executemany(
        'INSERT INTO users(username, password) VALUES (?,?)', users)

    # print all users from sqlite
    # for row in cur.execute("SELECT id, username, password FROM users"):
    #     print(row)

    con.commit()
    con.close()


def get_user(username, password):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    con.close()
    return {"id": user[0], "username": user[1], "password": user[2]}


def get_user_by_username(username):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    return user


def get_user_by_id(id):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cur.fetchone()
    con.close()
    return user


def create_user(username, password):
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    cur.execute("INSERT INTO users(username, password) VALUES (?,?)",
                (username, password))

    con.commit()
    con.close()
