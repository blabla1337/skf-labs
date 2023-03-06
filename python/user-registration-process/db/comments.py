import sqlite3


def seed_comments():
    comments = [('Michael', 'Nice picure!'),
                ('Adam', 'I like this post.'),
                ('Michael', 'I agree with you.'),
                ('Andrew', 'Where is this?'),
                ]

    con = sqlite3.connect("db.db")
    cur = con.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS comments
                (id INTEGER PRIMARY KEY, author, text)
                ''')
    cur.executemany(
        'INSERT INTO comments(author, text) VALUES (?,?)', comments)

    con.commit()
    con.close()


def get_comments():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM comments")
    comments = cur.fetchall()
    con.close()
    # make a list of dictionaries
    comments_list = []
    for comment in comments:
        comments_list.append(
            {"id": comment[0], "author": comment[1], "text": comment[2]})
    return comments_list


def create_comment(author, text):
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    cur.execute("INSERT INTO comments(author, text) VALUES (?,?)",
                (author, text))

    con.commit()
    con.close()


def update_comment(id, text):
    con = sqlite3.connect("db.db")
    cur = con.cursor()

    cur.execute("UPDATE comments SET text = ? WHERE id = ?",
                (text, id))

    con.commit()
    con.close()
