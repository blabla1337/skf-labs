from db.db import comments, users
from uuid import uuid4


def seed_db():
    init_users = ["Mike", "John", "Jane", "Mary", "Bob"]
    # Seed the database with some users
    if(users.count() == 0):
        new_users = [
            {"_id": uuid4().hex,
             "username": init_users[0], "password": "07RYbe$!9y11"},
            {"_id": uuid4().hex,
             "username": init_users[1], "password": "07RYbe$!9y22"},
            {"_id": uuid4().hex,
             "username": init_users[2], "password": "07RYbe$!9y23"},
            {"_id": uuid4().hex,
             "username": init_users[3], "password": "07RYbe$!9y24"},
            {"_id": uuid4().hex,
                "username": init_users[4], "password": "07RYbe$!9y25"}

        ]
        users.insert_many(new_users)

        # Seed the database with some comments
        if(comments.count() == 0):
            new_comments = [
                {"_id": uuid4().hex, "author": init_users[0],
                 "text": "Good picture!"},
                {"_id": uuid4().hex, "author": init_users[1], "text": "Nice!"},
                {"_id": uuid4().hex, "author": init_users[2], "text": "Cool!"},
                {"_id": uuid4().hex,
                 "author": init_users[3], "text": "Awesome!"},
                {"_id": uuid4().hex,
                    "author": init_users[4], "text": "Great!"}
            ]

            comments.insert_many(new_comments)
