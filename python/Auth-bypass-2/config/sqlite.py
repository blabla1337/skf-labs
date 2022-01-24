import sqlite3,os

def database_con():
    BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    db_path = os.path.join(BASE_DIR, "Database.db")
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
    return con