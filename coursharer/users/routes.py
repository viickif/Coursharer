from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from coursharer import db
from coursharer.models import Course, User
from coursharer.users.forms import (LoginForm, RegistrationForm,
                                    RequestResetForm, ResetPasswordForm,
                                    UpdateAccountForm)
from coursharer.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    courses = Course.query.order_by(Course.date_posted.desc()).paginate(page=page, per_page=5)
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('dashboard.html', name=current_user.username, image_file=image_file, courses=courses)

@users.route('/account_details', methods=['GET', 'POST'])
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
        print('Your account account has been updated!')
        return redirect(url_for('users.account_details'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('account_details.html', name=current_user.username, image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_courses(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    courses = Course.query.filter_by(author=user)\
        .order_by(Course.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_courses.html', courses=courses, user=user)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('users.dashboard'))
        else:
            print('Login unsuccessful...')

    return render_template('login.html', form=form)

@users.route('/signup', methods=['GET', 'POST'])
def signup():
    print('-1')
    form = RegistrationForm()
    print('0')
    if form.validate_on_submit():
        print('1')
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        print('2')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        print('3')
        db.session.add(new_user)
        print('4')
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
        print('login form is valid.')
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        print('An email has been sent with instructions to reset your password.')
        return redirect(url_for('users.login'))
    print('login form is invalid.')
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