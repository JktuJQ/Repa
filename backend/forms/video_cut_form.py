# Imports
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, ValidationError
import re


def validate_timecode(form, field):
    if not re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}$', field.data):
        raise ValidationError('Timecode must be in HH:MM:SS.mmm format')


class VideoCutForm(FlaskForm):
    label = SelectField('Доп-картинка в клип', choices=[("minecraft1", "Майнкрафт 1"), ("minecraft2", "Майнкрафт 2"),
                                                        ("subway_surf", "Сабвей сёрф")], validators=[])
    start_time = StringField('Начало отрезка', validators=[DataRequired(), validate_timecode])
    end_time = StringField('Конец отрезка', validators=[DataRequired(), validate_timecode])
    submit = SubmitField('Нарезать')
