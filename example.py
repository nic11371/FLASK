from flask import Flask, request
from flask import render_template

app = Flask(__name__)

users = [
    {'id': 1, 'name': 'mike'},
    {'id': 2, 'name': 'mishel'},
    {'id': 3, 'name': 'adel'},
    {'id': 4, 'name': 'keks'},
    {'id': 5, 'name': 'kamila'}
]


@app.route('/')
def hello_world():
    return 'Welcome to Nick!'


@app.get('/users/')
def get_users():
    query = request.args.get('query', '')
    filtered = [u for u in users if query in u['name']]
    return render_template(
        'users/index.html',
        users=filtered,
        search=query,
    )


@app.post('/users')
def post_users():
    return 'Users', 302


@app.route('/courses/<id>')
def courses_show(id):
    return f'Course id: {id}'


@app.route('/users/<id>')
def show_user(id):
    user = {
        'id': id,
        'name': f"user-{id}"
    }
    return render_template(
        'users/show.html',
        user=user,
    )
