from flask import Blueprint, json, jsonify, request, send_file
from .models import Post
from werkzeug.utils import secure_filename
from . import db
import os
import random

api = Blueprint("api", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uploads/")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def random_filename(filename):
    min_ = int(1e7)
    max_ = 99999999
    rand = str(random.randint(min_, max_)) + "." + filename.rsplit(".", 1)[1].lower()

    # Check if the filename is already in the database
    from sqlalchemy.orm import sessionmaker

    db_session_maker = sessionmaker(bind=db.engine)
    db_session = db_session_maker()
    while (
        db_session.query(Post).filter(Post.file_name == rand).limit(1).first()
        is not None
    ):
        rand = (
            str(random.randint(min_, max_)) + "." + filename.rsplit(".", 1)[1].lower()
        )

    return rand


@api.route("/images/", methods=["GET", "POST"])
def images():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return jsonify({"message": "No File"}), 400
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file.filename == "":
            return jsonify({"message": "No File Selected"}), 400

        if file and allowed_file(file.filename):
            print("saving")
            filename = random_filename(secure_filename(file.filename))
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        post = Post(title=request.form["title"], file_name=filename)
        db.session.add(post)
        db.session.commit()
        return jsonify({"image": post.json()}), 201
    elif request.method == "GET":
        posts = Post.query.all()
        return jsonify({"images": [post.json() for post in posts]}), 200


@api.route("/images/<int:image_id>", methods=["GET, DELTE"])
def image(image_id):
    if request.method == "GET":
        post = Post.query.filter_by(uuid=int(image_id)).first()
        return jsonify({"image": post.json()}), 200
    elif request.method == "DELETE":
        post = Post.query.filter_by(uuid=int(image_id)).first()
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Image Deleted"}), 200


@api.route("/files/<file_name>", methods=["GET"])
def file(file_name):
    return send_file(os.path.join(UPLOAD_FOLDER, file_name))
