import sqlite3


def seed_users():
    users = [('Michael', '07RYbe$!9y11', "admin"),
             ('Adam', '07RYbe$!9y12', "user"),
             ('Andrew', '07RYbe$!9y13', "user"),
             ]

    con = sqlite3.connect("db.db")
    cur = con.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, username, password, role)
                ''')
    cur.executemany(
        'INSERT INTO users(username, password, role) VALUES (?,?,?)', users)

    # print all users from sqlite
    for row in cur.execute("SELECT id, username, password, role FROM users"):
        print(row)

    con.commit()
    con.close()


def get_user(username, password):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    con.close()
    if not user:
        return user
    return {"id": user[0], "username": user[1], "password": user[2], "role": user[3]}


def get_user_by_username(username):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    if not user:
        return user
    return {"id": user[0], "username": user[1], "password": user[2], "role": user[3]}


def get_user_by_id(id):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cur.fetchone()
    con.close()
    if not user:
        return user
    return {"id": user[0], "username": user[1], "password": user[2], "role": user[3]}


def create_user(username, password, user="user"):
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    cur.execute("INSERT INTO users(username, password, role) VALUES (?,?,?)",
                (username, password, user))

    con.commit()
    con.close()


def get_customers():
    # list of customers with name, email, address, phone, and spending
    return [
        {
            "name": "John Doe",
            "email": "john@doe.com",
            "address": "123 Main St",
            "phone": "555-555-5555",
            "spending": "$100"
        },
        {
            "name": "Jane Doe",
            "email": "jane@doe.com",
            "address": "123 Main St",
            "phone": "555-555-5555",
            "spending": "$100"
        },
        {
            "name": "John Smith",
            "email": "john@smith.com",
            "address": "123 Main St",
            "phone": "555-555-5555",
            "spending": "$100"
        },
        {
            "name": "Jane Smith",
            "email": "jane@smith.com",
            "address": "123 Main St",
            "phone": "555-555-5555",
            "spending": "$100"
        },

    ]
