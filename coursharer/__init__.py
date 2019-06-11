from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail

from coursharer.config import Config


bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
from coursharer.models import User, Course

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bootstrap = Bootstrap(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from coursharer.users.routes import users
    from coursharer.courses.routes import courses
    from coursharer.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(courses)
    app.register_blueprint(main)

    return app