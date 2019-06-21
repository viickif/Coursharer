from flask import Blueprint, render_template, url_for
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():

    image_file = 'a'

    if current_user.is_authenticated:
        image_path = 'profile_pictures/' + current_user.image_file
        image_file = url_for('static', filename=image_path)

    return render_template('index.html', logged_in=current_user.is_authenticated, image_file=image_file)
