# 官方quickstart
import flask_sqlalchemy.record_queries
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
# echo the SQL statements to the console
# app.config["SQLALCHEMY_ECHO"] = True

# initialize the app with the extension
# create the extension
db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String)


# region Multi Conn Test
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///multi-test1.db'
# app.config['SQLALCHEMY_BINDS'] = {
#     'db1': 'sqlite:///multi-test2.db',
#     'db2': {
#         'url': 'sqlite:///multi-test3.db',
#     }
# }
#
# db = SQLAlchemy(app)
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     email = db.Column(db.String(120))
#
#
# class User1(db.Model):
#     __bind_key__ = 'db1'
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     email = db.Column(db.String(120))
#
#
# class User2(db.Model):
#     __bind_key__ = 'db2'
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     email = db.Column(db.String(120))

# endregion

# region reflect test
# using the exited database, by reflect
# with app.app_context():
#     db.reflect()


# # add a user
# class ExistedUser():
#     __table__ = db.Model.metadata.tables['user']
#
#
# # output existed table info
# print(ExistedUser.__table__.columns.keys())
# print(ExistedUser.__table__.columns.values())

# endregion

# create tables, drop tables before create
with app.app_context():
    db.drop_all()
    db.create_all()


# region check query record
@app.route("/record")
def record():
    records = flask_sqlalchemy.record_queries.get_recorded_queries()
    # output record info
    return "<br>".join([
        f"'info.statement: '{info.statement} 'info.parameters: '{info.parameters} "
        f"'info.start_time: '{info.start_time} 'info.end_time: '{info.end_time}"
        f"'info.duration: '{info.duration} 'info.location: '{info.location}\n"
        for info in records])


# endregion

# region query the database, CURD

# get all
@app.route("/users")
def get_users():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    records = flask_sqlalchemy.record_queries.get_recorded_queries()
    # output record info
    return jsonify(
        [{"info.statement": info.statement, "info.duration": info.duration, "info.location": info.location}
         for info in records])
    return "<br>".join([user.username for user in users])


# get one details
@app.route("/user/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return f"{user.username} has email {user.email}"


# create one
@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    user = User(username="test", email="test.com")
    db.session.add(user)
    db.session.commit()
    return f"Created user {user.username}"


# update one
@app.route("/update_user/<int:user_id>", methods=["GET", "PUT"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    user.username = "new username"
    db.session.commit()
    return f"Updated user {user.username}"


# delete one
@app.route("/delete_user/<int:user_id>", methods=["GET", "DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return f"Deleted user {user.username}"


# endregion

# run the app
if __name__ == "__main__":
    app.run()
