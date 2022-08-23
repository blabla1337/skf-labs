import sqlite3


def valid_login(username, password):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        result = cur.fetchone()
        return result is not None


def get_all_products():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM products')
        result = cur.fetchall()
        return result


def delete_product(product_id):
    with sqlite3.connect('database.db') as conn:
        conn.execute('DELETE FROM products WHERE id=?', (product_id, ))
        conn.commit()
        return True
