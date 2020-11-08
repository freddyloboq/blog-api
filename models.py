from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        # return super().__repr__()
        return "<User %r>" %self.name

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "bio": self.bio
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category", backref = db.backref("posts", lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("users",lazy=True))

    def __repr__(self):
        # return super().__repr__()
        return "<Post %r>" %self.name

    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "user_name": self.user_name,
            "publication_date": self.publication_date
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        # return super().__repr__()
        return "<Category %r>" %self.name

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name
        }
