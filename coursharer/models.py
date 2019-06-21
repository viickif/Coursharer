from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app

from coursharer import db, login_manager
import coursharer.constants as CONST

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(CONST.USERNAME_LENGTH), unique=True, nullable=False)
    image_file = db.Column(db.String(CONST.IMAGE_FILE_LENGTH), nullable=False, default='defaultMalePhoto.jpg')
    email = db.Column(db.String(CONST.EMAIL_LENGTH), unique=True, nullable=False)
    password = db.Column(db.String(CONST.PASSWORD_LENGTH), nullable=False)
    courses = db.relationship('Course', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=CONST.RESET_PASSWORD_EXPIRE_TIME):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}': '{self.email}'"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(CONST.TITLE_LENGTH), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # image_file = db.Column(db.String(CONST.IMAGE_FILE_LENGTH), nullable=False, default='lecture.jpg')

    def __repr__(self):
        return f"Course('{self.title}': '{self.description}'"
        
# @roles_required
# Instructor, Student, and Admin extending from User
