# Imports
from globals import *

from backend.application import application, db_session
from flask import render_template, session, url_for, redirect

from data.db_models import File, FileType


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


@application.route("/notes", methods=["GET"])
def notes():
    pass


@application.route("/cheatsheets", methods=["GET"])
def cheatsheets():
    pass


@application.route("/textbooks", methods=["GET"])
def textbooks():
    pass


@application.route("/videos", methods=["GET"])
def videos():
    pass


@application.route("/clips", methods=["GET"])
def clips():
    pass
