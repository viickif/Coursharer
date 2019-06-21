from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import InputRequired


class CourseForm(FlaskForm):
    title = StringField('Course Title', validators=[InputRequired()])
    content = TextAreaField('Description', validators=[InputRequired()])
    # image_file = FileField('Update Course Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Create')
