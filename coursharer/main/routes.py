from flask import Blueprint, render_template, url_for, request
from flask_login import current_user

import coursharer.constants as CONST
from coursharer import db
from coursharer.models import Course, User
main = Blueprint("main", __name__)


@main.route("/search", methods=['GET'])
def search():
    query = request.args['q']
    page = request.args.get("page", CONST.DEFAULT_PAGE, type=int)
    courses = Course.query.filter(Course.title.contains(query)).order_by(Course.date_posted.desc()).paginate(
        page=page, per_page=CONST.COURSES_PER_PAGE
    )

    profile_photo_file = ""
    name = ""

    if current_user.is_authenticated:
        profile_photo_path = "profile_photos/" + current_user.profile_photo
        profile_photo_file = url_for("static", filename=profile_photo_path)
        name = current_user.username

    return render_template(
        "dashboard.html",
        logged_in=current_user.is_authenticated,
        name=name,
        profile_photo_file=profile_photo_file,
        courses=courses,
        title="Search Results",
        header=f"Search Results for: {query}",
        empty_courses_msg="No results.",
    )


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