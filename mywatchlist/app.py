from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


@app.route('/')
def hello():
    """
    Returns a greeting message.
    """
    return render_template('index.html', name=name, movies=movies)


@app.route('/user/<username>')
def user_profile(username):
    return f'User: {escape(username)}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post: {post_id}'
    
if __name__ == '__main__':
    app.run(debug=True)
