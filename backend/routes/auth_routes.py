# Imports
from backend.application import application, db_session
from flask import render_template, session, url_for, redirect, flash

from data.db_models import User

from backend.forms.auth_forms import *


@application.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_session().query(User).filter(User.username == form.username.data).first()
        if user and user.password == form.password.data:
            session["logged_in"] = True
            session["id"] = user.id
            session["username"] = user.username
            session["name"] = user.name
            flash("Успешный вход в аккаунт", "success")
            return redirect(url_for("dashboard"))

        flash("Неверное имя пользователя или пароль", "error")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)


@application.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("Выход из аккаунта был успешен", "success")
    return redirect(url_for("login"))


@application.route("/register", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data

        if username in db_session().query(User.username).all():
            flash("Такое имя пользователя уже занято", "error")
        else:
            db_session().add(User(username=username, password=password, name=name))
            db_session().commit()
        flash("Аккаунт был создан. Теперь требуется вход", "success")
        return redirect(url_for("login"))

    return render_template("registration.html", form=form)
