from flask_wtf import FlaskForm
from wtforms import SubmitField


class NotepadForm(FlaskForm):
    submit = SubmitField('Save notepad')
