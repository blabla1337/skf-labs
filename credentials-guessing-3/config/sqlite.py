import sqlite3

def database_con():
    with sqlite3.connect("Database.db") as con:
        cur = con.cursor()
    return con