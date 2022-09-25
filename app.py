from flask import Flask
from models import db
from views.home import home


# Config
app = Flask(__name__)
app.config["DATABASE_URL"] = "sqlite:///db.sqlite3"
app.config["SECRET_KEY"] = "asmduianwdias dapdwaokd apd adao"
db.init_app(app)


# Blueprints
app.register_blueprint(home, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

