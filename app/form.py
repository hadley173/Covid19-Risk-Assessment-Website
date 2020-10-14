from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class RiskForm(FlaskForm):
    statename = StringField('Name of state', validators=[DataRequired()])
    submit = SubmitField('Submit')