from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired


class CleaningForm(FlaskForm):
    instrument = StringField('Machine Name', validators=[DataRequired()], description='For MS or LC.')
    maintenance_type = StringField('Maintenance Type', validators=[DataRequired()], description='Cleaning, Bake out, etc.')
    predicted_duration = FloatField('Predicted Duration (hours)', validators=[DataRequired()], description='Between maintenance start and next recording start.')
    submitted_by = StringField('Job Requested By', validators=[DataRequired()], description='Your name here.')
