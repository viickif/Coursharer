from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired


class CourseForm(FlaskForm):
    title = StringField('Course Title', validators=[InputRequired()])
    content = TextAreaField('Description', validators=[InputRequired()])
    submit = SubmitField('Create')
