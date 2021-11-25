from . import db
from sqlalchemy.sql import func
import random


# Random UUID generation
def random_integer():
    min_ = int(1e7)
    max_ = 99999999
    rand = random.randint(min_, max_)

    # Check if the UUID is already in the database
    from sqlalchemy.orm import sessionmaker

    db_session_maker = sessionmaker(bind=db.engine)
    db_session = db_session_maker()
    while db_session.query(Post).filter(Post.uuid == rand).limit(1).first() is not None:
        rand = random.randint(min_, max_)

    return rand


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Integer, default=random_integer, unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, default=0, nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)

    def json(self):
        return {
            "uuid": self.uuid,
            "title": self.title,
            "file_name": self.file_name,
            "views": self.views,
            "likes": self.likes,
        }
