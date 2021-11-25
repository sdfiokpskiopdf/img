from flask import Blueprint, json, jsonify, request
from .models import Post
from werkzeug.utils import secure_filename
from . import db
import os

api = Blueprint("api", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uploads/")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
            filename = secure_filename(file.filename)
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
