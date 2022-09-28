from flask import Flask, render_template
from flask_login import LoginManager
from models import db, Usuario
from views.home import home
from views.user import user
from views.api import api


# Config
app = Flask(__name__)
app.config["DATABASE_URL"] = "sqlite:///db.sqlite3"
app.config["SECRET_KEY"] = "asmduianwdias dapdwaokd apd adao"
db.init_app(app)


#Login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    try:
        user = Usuario.get(Usuario.id == user_id)
        return user
    except:
        return

# Blueprints
app.register_blueprint(home, url_prefix="/")
app.register_blueprint(user, url_prefix="/dashboard")
app.register_blueprint(api, url_prefix="/")


# Error handlers
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

# Error handlers
@app.errorhandler(401)
def not_authorized(e):
  return render_template("401.html")

# Error handlers
@app.errorhandler(502)
def not_work(e):
  return render_template("502.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

