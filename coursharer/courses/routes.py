from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from coursharer import db
from coursharer.courses.forms import CourseForm
from coursharer.models import Course

courses = Blueprint('courses', __name__)

@courses.route('/course/new', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        post = Course(title=form.title.data, description=form.content.data,
                      author=current_user)
                    #   , profile_photo_file=form.profile_photo.data)

        db.session.add(post)
        db.session.commit()
        print('Your course has been created!')

        return redirect(url_for('users.dashboard'))
    
    profile_photo_path = 'profile_photos/' + current_user.profile_photo
    profile_photo = url_for('static', filename=profile_photo_path)

    return render_template('create_course.html', form=form,
                            title='Create New Course', name=current_user.username, profile_photo_file=profile_photo_file)

@courses.route("/course/<int:course_id>")
def course(course_id):
    course = Course.query.get_or_404(course_id)
    profile_photo_path = 'profile_photos/' + current_user.profile_photo
    profile_photo_file = url_for('static', filename=profile_photo_path)

    return render_template('course.html', course=course, name=current_user.username, profile_photo_file=profile_photo_file)


@courses.route("/course/<int:course_id>/update", methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    course = Course.query.get_or_404(course_id)

    if course.author != current_user:
        abort(403)

    form = CourseForm()

    if form.validate_on_submit():
        course.title = form.title.data
        course.description = form.content.data
        db.session.commit()
        print('Your course has been updated')

        return redirect(url_for('courses.courses.course', course_id=course_id))
    elif request.method == 'GET':
        form.title.data = course.title
        form.content.data = course.description

    profile_photo_path = 'profile_photos/' + current_user.profile_photo
    profile_photo_file = url_for('static', filename=profile_photo_path)

    return render_template('create_course.html', title='Update Course', form=form, name=current_user.username, profile_photo_file=profile_photo_file)


@courses.route("/course/<int:course_id>/delete", methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)

    if course.author != current_user:
        abort(403)

    db.session.delete(course)
    db.session.commit()
    print('Your course has been deleted!')

    return redirect(url_for('users.dashboard'))
