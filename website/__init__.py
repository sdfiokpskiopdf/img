from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__, static_url_path="", static_folder="frontend/build")
    app.config["SECRET_KEY"] = """w[n0l$;TB8IiA|hFuk:<V>M_6'ngdd"""
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_NAME
    db.init_app(app)

    @app.route("/", defaults={"path": ""})
    def serve(path):
        return send_from_directory(app.static_folder, "index.html")

    from .api import api

    app.register_blueprint(api, url_prefix="/api/v1")

    from .models import Post

    create_database(app)

    return app


def create_database(app):
    if not os.path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("[SUCCESS] Database Created")
    else:
        print("[INFO] Database Already Exists")
