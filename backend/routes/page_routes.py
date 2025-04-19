# Imports
from globals import *

from backend.application import application, db_session
from flask import render_template, session, url_for, redirect

from data.db_models import Note


@application.route("/", methods=["GET"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@application.route("/dashboard", methods=["GET"])
def dashboard():
    if not session.get("logged_in"):
        print("not logged in")
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        file_types=FILE_TYPES,
        file_data={
            "notes":
                db_session().query(Note).filter(Note.type == 1).all(),
            "cheatsheets":
                db_session().query(Note).filter(Note.type == 2).all(),
        })

