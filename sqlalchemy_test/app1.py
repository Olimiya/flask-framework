import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)


@app.route('/create_user')
def create_user():
    # 创建一个新的用户
    user = User(name='John', age=25)
    db.session.add(user)
    db.session.commit()
    return 'User created successfully!'


@app.route('/get_user/<int:user_id>')
def get_user(user_id):
    # 根据用户ID查询用户信息
    user = User.query.get(user_id)
    if user:
        return f'User name: {user.name}, age: {user.age}'
    else:
        return 'User not found!'


@app.route('/update_user/<int:user_id>')
def update_user(user_id):
    # 根据用户ID更新用户信息
    user = User.query.get(user_id)
    if user:
        user.age = 30
        db.session.commit()
        return 'User updated successfully!'
    else:
        return 'User not found!'


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    # 根据用户ID删除用户信息
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return 'User deleted successfully!'
    else:
        return 'User not found!'


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息
