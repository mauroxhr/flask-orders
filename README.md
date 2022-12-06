This web application was developed in Python. App is in development.

# Step one
pip install -r requirements.txt

# Step two
pw_migrate create --auto --database "sqlite:///db.sqlite3" --auto-source models initial

# If migrations exist
pw_migrate migrate --database "sqlite:///db.sqlite3"

# step three
python app.py


---

You can test this project in [xhlar](https://api.xhlar.com)
