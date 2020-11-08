import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, User, Category, Post

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, "test.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =  False
app.config["DEBUG"] = True
app.config["ENV"] = "development"

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)#init, migrate, upgrade
CORS(app)

@app.route("/user/<int:id>", methods=["GET", "DELETE", "PUT"])
@app.route("/user", methods=["POST"])
def user(id=None):
    if id is not None:
        if request.method == "GET":
            user = User.query.filter_by(id=id).first()
            return jsonify(user.serialize()), 200
        if request.method == "PUT":
            user = User.query.get(id)
            user.bio = request.json.get("bio")
            db.session.commit()
            return jsonify({"msg": "user updated"}), 200
        if request.method == "DELETE":
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return jsonify({"msg": "user deleted"}), 200
    elif request.method == "POST":
        user = User()
        user.name = request.json.get("name")
        user.age = request.json.get("age")
        user.bio = request.json.get("bio")
        user.password = request.json.get("password")
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 200
    else:
        users = User.query.all()
        users = list(map(lambda user: user.serialize(), users))
        return jsonify(users), 200

if __name__ == "__main__":
    manager.run()