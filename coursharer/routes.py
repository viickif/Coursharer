import os
import secrets
from PIL import Image
from flask import render_template, redirect, url_for, request, abort
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from coursharer import app, bootstrap, db, login_manager
from coursharer.models import User, Course
from coursharer.forms import LoginForm, RegisterForm, UpdateAccountForm, CourseForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>' #flash error

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return render_template('login.html', form=form)

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    courses = Course.query.all()
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('dashboard.html', name=current_user.username, image_file=image_file, courses=courses)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_fn)

    output_size = (125, 125)
    im = Image.open(form_picture)
    im.thumbnail(output_size)
    im.save(picture_path)

    return picture_fn


@app.route('/account_details', methods=['GET', 'POST'])
@login_required
def account_details():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account_details'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('account_details.html', name=current_user.username, image_file=image_file, form=form)

@app.route('/course/new', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        post = Course(title=form.title.data, description=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_course.html', form=form, title='Create New Course')

@app.route("/course/<int:course_id>")
def course(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course.html', course=course)


@app.route("/course/<int:course_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('course', course_id=course_id))
    elif request.method == 'GET':
        form.title.data = course.title
        form.content.data = course.description
    return render_template('create_course.html', title='Update Course', form=form)


@app.route("/course/<int:course_id>/delete", methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.author != current_user:
        abort(403)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('dashboard'))



