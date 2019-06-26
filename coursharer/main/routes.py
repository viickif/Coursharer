from flask import Blueprint, render_template, url_for
from flask_login import current_user

main = Blueprint("main", __name__)


@main.route("/")
def index():

    profile_photo_file = ""
    name = ""

    if current_user.is_authenticated:
        profile_photo_path = "profile_photos/" + current_user.profile_photo
        profile_photo_file = url_for("static", filename=profile_photo_path)
        name = current_user.username

    return render_template(
        "index.html",
        logged_in=current_user.is_authenticated,
        profile_photo_file=profile_photo_file,
        name=name
    )
