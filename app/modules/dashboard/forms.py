from flask_wtf import FlaskForm
from wtforms import SubmitField


class DashboardForm(FlaskForm):
    submit = SubmitField('Submit')