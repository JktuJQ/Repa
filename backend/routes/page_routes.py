# Imports
from globals import *

from backend.application import application, db_session
from flask import render_template, session, url_for, redirect, flash, request
from werkzeug.utils import secure_filename
from sqlalchemy import func

import os

from data.db_models import File, FileType, User

from backend.forms.download_form import DownloadFileForm
from backend.forms.update_form import UpdateFileForm

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

    file_data = {}
    for file_type in FILE_TYPES:
        files = list(map(file_info, db_session().query(File).filter(
            File.file_type_id == db_session().query(FileType).filter(
                FileType.type == file_type).first().id).order_by(File.id.desc())
                         .all()))
        for file in files:
            file_path = f"frontend/static{file['link']}"
            file_type = db_session().query(FileType).filter(FileType.id == file['file'].file_type_id).first().type
            file['file_type'] = file_type
            if file_type not in ['videos', 'clips']:
                if file_path.lower().endswith('.pdf'):
                    file['preview'] = url_for('static', filename='assets/pdf_preview.png')
                else:
                    file['preview'] = url_for('static', filename=file['link'].lstrip('/'))
            else:
                file['preview'] = url_for('static', filename='assets/default_preview.png')
        file_data[file_type] = files

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        file_types=FILE_TYPES,
        file_data=file_data
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


@application.route("/unified_catalog", methods=["GET"])
def unified_catalog():
    query = request.args.get('q', '').strip()

    search_results = db_session().query(File).join(User).filter(
        (File.name.ilike(f'%{query}%')) |
        (File.subject.ilike(f'%{query}%')) |
        (User.username.ilike(f'%{query}%'))
    ).order_by(File.created_at.desc()).all()

    files = [
        file_info(file)
        for file in search_results
    ]
    for file in files:
        file_path = f"frontend/static{file['link']}"
        file_type = db_session().query(FileType).filter(FileType.id == file['file'].file_type_id).first().type
        file['file_type'] = file_type
        if file_type not in ['videos', 'clips']:
            if file_path.lower().endswith('.pdf'):
                file['preview'] = url_for('static', filename='assets/pdf_preview.png')
            else:
                file['preview'] = url_for('static', filename=file['link'].lstrip('/'))
        else:
            file['preview'] = url_for('static', filename='assets/default_preview.png')

    return render_template("unified_catalog.html", files=files, search_query=query)


@application.route("/catalog/<string:file_type>", methods=["GET"])
def catalog(file_type: str):
    if file_type not in FILE_TYPES:
        return "Неправильный запрос", 400

    files = list(
        file_info(file)
        for file in db_session().query(File).filter(
            File.file_type_id == db_session().query(FileType).filter(FileType.type == file_type).first().id).all()
    )

    subjects = {}
    for file in files:
        subject = file['file'].subject or "Без темы"
        if subject not in subjects:
            subjects[subject] = []
        subjects[subject].append(file)

    sorted_subjects = sorted(subjects.items(), key=lambda x: len(x[1]), reverse=True)

    for _ in sorted_subjects:
        for file in files:
            file_path = f"frontend/static{file['link']}"
            file_type = db_session().query(FileType).filter(FileType.id == file['file'].file_type_id).first().type
            file['file_type'] = file_type
            if file_type not in ['videos', 'clips']:
                if file_path.lower().endswith('.pdf'):
                    file['preview'] = url_for('static', filename='assets/pdf_preview.png')
                else:
                    file['preview'] = url_for('static', filename=file['link'].lstrip('/'))
            else:
                file['preview'] = url_for('static', filename='assets/default_preview.png')

    return render_template(
        "catalog.html",
        file_type=file_type,
        file_type_ru=FILE_TYPES_RU[FILE_TYPES.index(file_type)],
        subjects=sorted_subjects
    )


@application.route("/file_detail/<int:file_id>", methods=["GET"])
def file_detail(file_id: int):
    file = file_info(db_session().query(File).filter(File.id == file_id).first())
    initial_file_type = db_session().query(FileType).filter(
        FileType.id == file["file"].file_type_id).first().type

    related_files = list(file_info(f) for f in db_session().query(File).filter(
        (File.subject == file["file"].subject) | (File.author_id == file["file"].author_id)).filter(
        File.id != file["file"].id).all())
    for related in related_files:
        file_path = f"frontend/static{related['link']}"
        file_type = db_session().query(FileType).filter(FileType.id == related['file'].file_type_id).first().type
        related['file_type'] = file_type
        if file_type not in ['videos', 'clips']:
            if file_path.lower().endswith('.pdf'):
                related['preview'] = url_for('static', filename='assets/pdf_preview.png')
            else:
                related['preview'] = url_for('static', filename=related['link'].lstrip('/'))
        else:
            related['preview'] = url_for('static', filename='assets/default_preview.png')

    return render_template(
        "file_detail.html",
        file=file,
        file_type=initial_file_type,
        related_files=related_files
    )


@application.route("/update_file/<int:file_id>", methods=["GET", "POST"])
def update_file(file_id: int):
    file = db_session().query(File).filter(File.id == file_id).first()
    form = UpdateFileForm(obj=file)

    if form.validate_on_submit():
        file.name = form.name.data
        file.description = form.description.data
        file.subject = form.subject.data
        file.create_at = datetime.today().strftime('%Y-%m-%d')

        if form.file.data:
            file_path = f"frontend/static{(file_info(file))['link']}"
            if os.path.exists(file_path):
                os.remove(file_path)

            form.file.save(file_path)

            file.filename = file_path
            file.filetype = db_session().query(FileType).filter(FileType.type == form.file_type.data).first().id

        db_session().commit()
        flash("Файл успешно обновлен", "success")
        return redirect(url_for("file_detail", file_id=file.id))

    return render_template('update_file.html', form=form, file=file)


@application.route("/delete_file/<int:file_id>", methods=["GET", "POST"])
def delete_file(file_id: int):
    file = db_session().query(File).filter(File.id == file_id).first()

    if not file:
        flash("Такой записи не существует", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        if request.form.get("confirm") == "yes":
            try:
                file_path = f"frontend/static/assets/{db_session().query(FileType).filter(FileType.id == file.file_type_id).first().type}/{file.filename}"
                if os.path.exists(file_path):
                    os.remove(file_path)

                db_session().delete(file)
                db_session().commit()
                flash("Удаление прошло успешно", "success")
            except Exception as e:
                db_session().rollback()
                flash(f"Ошибка с удалением", "error")
        return redirect(url_for("dashboard"))

    return render_template("delete_file.html", file=file)
