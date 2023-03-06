from db.users import seed_users
from db.comments import seed_comments


def seed_db():
    seed_users()
    seed_comments()
