import os
import secrets

from flask_login import current_user
from flask import current_app, url_for
from flask_mail import Message
from PIL import Image

from coursharer import mail, db

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pictures', picture_fn)

    output_size = (125, 125)
    im = Image.open(form_picture)
    im.thumbnail(output_size)
    im.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='coursharer@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
    print('An email has been sent with instructions to reset your password.')

def update_user_info(form):
    if form.picture.data:
        picture_file = save_picture(form.picture.data)
        current_user.image_file = picture_file

    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    print('Your account account has been updated!')
