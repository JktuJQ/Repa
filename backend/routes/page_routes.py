# Imports
from globals import *

from backend.application import application, db_session
from flask import render_template, session, url_for, redirect

from data.db_models import File, FileType, User


@application.route("/", methods=["GET"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@application.route("/dashboard", methods=["GET"])
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        file_types=FILE_TYPES,
        file_data={
            file_type: db_session().query(File).filter(
                File.file_type_id == db_session().query(FileType).filter(FileType.type == file_type).first().id)
            .all()
            for file_type in FILE_TYPES
        }
    )


@application.route("/catalog/<string:file_type>", methods=["GET"])
def catalog(file_type: str):
    if file_type not in FILE_TYPES:
        return "Неправильный запрос", 400

    return render_template(
        "catalog.html",
        file_type=file_type,
        file_type_ru=FILE_TYPES_RU[FILE_TYPES.index(file_type)],
        files=[
            {
                "file": file,
                "author": db_session().query(User).filter(User.id == file.author_id).first().username,
                "link": url_for('static', filename=f"assets/{file_type}/{file.filename}")
            }
            for file in db_session().query(File).filter(
                File.file_type_id == db_session().query(FileType).filter(FileType.type == file_type).first().id).all()
        ]
    )


@application.route("/file_detail/<int:file_id>")
def file_detail(file_id: int):
    return render_template("file_detail.html")
