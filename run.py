from coursharer import create_app
from datetime import timedelta
app = create_app()
app.PERMANENT_SESSION_LIFETIME = timedelta(seconds=7)
# app.REMEMBER_COOKIE_DURATION = timedelta(seconds=2)
# app.config["REMEMBER_COOKIE_DURATION"] = timedelta(seconds=2)
if __name__ == '__main__':
    app.run(debug=True)