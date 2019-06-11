# Coursharer

> Inspiration: to create a platform for instructors to share their whole file every frame instead of just their screen. This will allow students to see what the instructor talked about in the previous screen simply by scrolling rather than rewinding the video and the fast forwarding it to its original position

#### Run

#### Linux and Mac

```terminal
export EMAIL_USER={company email}
export EMAIL_PASS={company email password}
export FLASK_APP=run.py
export SECRET_KEY='daa225d7b4d306991af1f66cc3656352'
export SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
flask run
```

#### Windows cmd

```Linux
set FLASK_APP=coursharer.py
set FLASK_ENV=development
flask run
```

EMAIL_USER

EMAIL_PASS

### Installation

Install `Python3` and `Pip3`

```Linux
pip3 install flask
pip3 install flask_bootstrap
pip3 install flask_wtf
pip3 install flask_sqlalchemy
pip3 install  flask_login
```

Install SQLite

If you are using VSC “ode, complete the following to avoid Flask-SQLAlchemy Pylint errors:

1. Run `pip install pylint-flask` in terminal
2. Press `Ctrl + Shift + P`. Then enter “Preferences: Open Settings (JSON)”
3. Add "python.linting.pylintArgs": ["--load-plugins", "pylint_flask"]



Should add in requirements when implemented

Flask-Mail==0.9.1

blinker==1.4

certifi==2016.2.28

cffi==1.11.5

click==6.7

itsdangerous==0.24

Jinja2==2.10

MarkupSafe==1.0

Pillow==5.3.0

pycparser==2.18

six==1.11.0

Werkzeug==0.14.1