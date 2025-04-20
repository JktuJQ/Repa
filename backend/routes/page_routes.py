# Imports
from globals import *

from backend.application import application, db_session
from flask import render_template, session, url_for, redirect, flash, request
from werkzeug.utils import secure_filename
from sqlalchemy import func

from data.db_models import File, FileType, User

from backend.forms.download_form import DownloadFileForm

from datetime import datetime


@application.route("/", methods=["GET"])
def index():
    """Корень веб-приложения."""
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@application.route("/dashboard", methods=["GET"])
def dashboard():
    """Главная страница сайта."""
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        file_types=FILE_TYPES,
        file_data={
            file_type: db_session().query(File).filter(
                File.file_type_id == db_session().query(FileType).filter(
                    FileType.type == file_type).first().id).order_by(File.id.desc())
            .all()
            for file_type in FILE_TYPES
        }
    )


@application.route('/download', methods=["GET", 'POST'])
def file_download():
    """Загружает файлы на сервис."""
    form = DownloadFileForm()
    form.file_type.data = request.args.get("chosen") if request.args.get("chosen") in FILE_TYPES else FILE_TYPES[0]
    if form.validate_on_submit():
        try:
            file = form.file.data
            filename, extension = secure_filename(file.filename).split(".")

            file_type = form.file_type.data
            if not (file_type in FILE_TYPES[:3] and extension in ("jpg", "jpeg", "png", "pdf") or
                    file_type in FILE_TYPES[3:] and extension in ("mov", "mp4", "mkv")):
                flash("Некорректное расширение файла.", "error")
                return render_template("file_download.html", form=form)

            db_session().add(
                File(name=form.name.data, created_at=datetime.today().strftime('%Y-%m-%d'), author_id=session["id"],
                     file_type_id=db_session().query(FileType).filter(FileType.type == form.file_type.data).first().id,
                     filename=filename + "(" + str(len(
                         db_session().query(File).filter(
                             File.filename.like(f"{filename.split('.')[0]}%")).all())) + ")." + extension,
                     description=form.description.data, subject=form.subject.data))
            db_session().commit()

            flash("Загрузка прошла успешно", "success")
            created_file = db_session().query(File).filter(
                File.id == db_session().query(func.max(File.id)).scalar()).first()
            file.save(f"frontend/static/assets/{form.file_type.data}/{created_file.filename}")
            return redirect(
                url_for("file_detail", file_id=created_file.id))

        except Exception as e:
            print(e)
            flash(f"Ошибка обработки файла", "error")
            return render_template("file_download.html", form=form)

    return render_template("file_download.html", form=form)


def file_info(file: File):
    """Возвращает информацию о файле."""
    return {
        "file": file,
        "author": db_session().query(User).filter(User.id == file.author_id).first().username,
        "link": f"/assets/{db_session().query(FileType).filter(FileType.id == file.file_type_id).first().type}/{file.filename}"
    }


@application.route("/catalog/<string:file_type>", methods=["GET"])
def catalog(file_type: str):
    if file_type not in FILE_TYPES:
        return "Неправильный запрос", 400

    return render_template(
        "catalog.html",
        file_type=file_type,
        file_type_ru=FILE_TYPES_RU[FILE_TYPES.index(file_type)],
        files=[
            file_info(file)
            for file in db_session().query(File).filter(
                File.file_type_id == db_session().query(FileType).filter(FileType.type == file_type).first().id).all()
        ]
    )


@application.route("/file_detail/<int:file_id>", methods=["GET"])
def file_detail(file_id: int):
    file = file_info(db_session().query(File).filter(File.id == file_id).first())
    file_type = db_session().query(FileType).filter(
        FileType.id == file["file"].file_type_id).first().type
    return render_template(
        "file_detail.html",
        file=file,
        file_type=file_type,
        related_files=db_session().query(File).filter(
            (File.subject == file["file"].subject) | (File.author_id == file["file"].author_id)).all()
    )
