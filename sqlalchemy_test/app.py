# 官方quickstart

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String)

with app.app_context():
    db.drop_all()
    db.create_all()

# query the database

# get all
@app.route("/users")
def get_users():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return "<br>".join([user.username for user in users])

# get one detals
@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return f"{user.username} has email {user.email}"

# create one
@app.route("/users", methods=["POST"])
def create_user():
    user = User(username="test", email="test.com")
    db.session.add(user)
    db.session.commit()
    return f"Created user {user.username}"

# update one
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    user.username = "new username"
    db.session.commit()
    return f"Updated user {user.username}"

# delete one
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return f"Deleted user {user.username}"

# run the app
if __name__ == "__main__":
    app.run()