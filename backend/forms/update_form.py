# Imports
from globals import *

from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length

from flask_wtf.file import FileAllowed


class UpdateFileForm(FlaskForm):
    """Форма загрузки."""

    file_type = SelectField(
        "Тип конспекта",
        choices=list(zip(FILE_TYPES, list(map(lambda x: x.capitalize(), FILE_TYPES_RU)))),
        validators=[DataRequired()],
        render_kw={"placeholder": "Выберите тип заметки"}
    )

    name = StringField(
        "Название",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ],
        render_kw={"placeholder": "Введите название конспекта"}
    )

    subject = StringField(
        "Учебный предмет",
        validators=[Length(max=100)],
        render_kw={"placeholder": "Введите учебный предмет"}
    )

    description = TextAreaField(
        "Описание",
        validators=[Length(max=500)],
        render_kw={
            "placeholder": "Введите описание",
            "rows": 4
        }
    )

    file = FileField(
        "Файл",
        validators=[
            FileAllowed(["pdf", "jpg", "jpeg", "png", "mp4"],
                        "Этот тип не поддерживается")
        ],
        render_kw={"accept": ".pdf,.jpg,.jpeg,.png,.mp4"}
    )

    submit = SubmitField("Загрузить")