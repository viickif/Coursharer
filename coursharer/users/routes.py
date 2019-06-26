from flask import Blueprint, flash, redirect, render_template, request, url_for,session
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

import coursharer.constants as CONST
from coursharer import db
from coursharer.models import Course, User
from coursharer.users.forms import (LoginForm, RegistrationForm,
                                    RequestResetForm, ResetPasswordForm,
                                    UpdateAccountForm)
from coursharer.users.utils import (save_picture, send_reset_email,
                                    update_user_info)
from datetime import timedelta
                    

users = Blueprint('users', __name__)

@users.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', CONST.DEFAULT_PAGE, type=int)
    courses = Course.query.order_by(Course.date_posted.desc())\
        .paginate(page=page, per_page=CONST.COURSES_PER_PAGE)

    profile_photo_path = 'profile_photos/' + current_user.profile_photo
    profile_photo_file = url_for('static', filename=profile_photo_path)

    return render_template('dashboard.html', name=current_user.username,
                            profile_photo_file=profile_photo_file, courses=courses)

@users.route('/account_details', methods=['GET', 'POST'])
@login_required
def account_details():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        update_user_info(form)

        return redirect(url_for('users.account_details'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_photo_path = 'profile_photos/' + current_user.profile_photo
    profile_photo_file = url_for('static', filename=profile_photo_path)

    return render_template('account_details.html', name=current_user.username,
                            profile_photo_file=profile_photo_file, form=form)


@users.route("/user/<string:username>")
def user_courses(username):
    page = request.args.get('page', CONST.DEFAULT_PAGE, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    courses = Course.query.filter_by(author=user)\
        .order_by(Course.date_posted.desc())\
        .paginate(page=page, per_page=CONST.COURSES_PER_PAGE)

    profile_photo_path = 'profile_photos/' + current_user.profile_photo
    profile_photo_file = url_for('static', filename=profile_photo_path)

    return render_template('user_courses.html', courses=courses, profile_photo_file=profile_photo_file, name=username, curr_username=current_user.username)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
                # login_user(user, remember=form.remember.data, duration=timedelta(hours=5))
                login_user(user, remember=False, duration=None, force=False, fresh=True)
                session.permanent = True
                return redirect(url_for('users.dashboard'))
        else:
            print('Login unsuccessful...')

    return render_template('login.html', form=form)

@users.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        print('Your account has been created!')

        return render_template('index.html')
    return render_template('signup.html', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)

        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))

    user = User.verify_reset_token(token)

    if user is None:
        print('That is an invalid or expired token.')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user.password = hashed_password
        db.session.commit()
        print('Your password has been updated! You are now able to log in.')

        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form)
