# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Форма для входа в аккаунт."""

    username = StringField(
        "Имя пользователя",
        validators=[
            DataRequired(),
            Length(min=4, message="Имя пользователя должно быть длинной минимум в 4 символа")
        ]
    )
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=8, message="Пароль должен быть длинной минимум в 8 символов")
        ]
    )
    submit = SubmitField("Войти")


class RegistrationForm(FlaskForm):
    """Форма для регистрации аккаунта."""

    username = StringField(
        "Имя пользователя",
        validators=[
            DataRequired(),
            Length(min=4, message="Имя пользователя должно быть длинной минимум в 4 символа")
        ]
    )
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=8, message="Пароль должен быть длинной минимум в 8 символов")
        ]
    )
    name = StringField(
        "Имя",
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField("Зарегистрировать")
