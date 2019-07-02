# Coursharer

> Inspiration: to create a platform for instructors to share their whole file every frame instead of just their screen. This will allow students to see what the instructor talked about in the previous screen simply by scrolling rather than rewinding the video and the fast forwarding it to its original position

#### Run
```
docker-compose up EMAIL_USER={company email} EMAIL_PASS={company email password}
```


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
set EMAIL_USER={company email}
set EMAIL_PASS={company email password}
set FLASK_APP=run.py
set SECRET_KEY='daa225d7b4d306991af1f66cc3656352'
set SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
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
pip3 install  flask_mail
```
