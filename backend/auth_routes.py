# Imports
from backend.application import application
from flask import render_template, session, url_for, redirect, request, flash


@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if True:  # username in users and users[username]["password"] == password:
            session["logged_in"] = True
            # session["username"] = users[username]["name"]
            # session["email"] = users[username]["email"]
            flash("Успешный вход в аккаунт", "success")
            return redirect(url_for("dashboard"))
        # else:
        #    flash("Неверное имя пользователя или пароль", "error")
    else:
        return render_template("login.html")


@application.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("Выход из аккаунта был успешен", "success")
    return redirect(url_for("login"))


@application.route("/register", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        email = request.form.get("email")

        # if username in users:
        #    flash("Username already exists", "error")
        # else:
        #    users[username] = {
        #        "password": password,
        #        "name": name,
        #        "email": email
        #    }
        flash("Аккаунт был создан. Теперь требуется вход", "success")
        return redirect(url_for("login"))

    return render_template("registration.html")
