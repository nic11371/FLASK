from flask import Flask, redirect, request, url_for
from flask import render_template
import json
import uuid

app = Flask(__name__)

users = [
    {'id': 1, 'name': 'mike'},
    {'id': 2, 'name': 'mishel'},
    {'id': 3, 'name': 'adel'},
    {'id': 4, 'name': 'keks'},
    {'id': 5, 'name': 'kamila'}
]


@app.route('/')
def index():
    return 'Welcome to Nick!'


@app.get('/users')
def get_users():
    query = request.args.get('query', '')
    filtered = [u for u in users if query in u['name']]
    return render_template(
        'users/index.html',
        users=filtered,
        search=query,
    )


@app.post('/users')
def users_post():
    user_data = request.form.to_dict()
    errors = validate(user_data)
    if errors:
        return render_template(
            'users/new.html',
            user=user_data,
            errors=errors
        )
    id = str(uuid.uuid4())
    user = {
        'id': id,
        'name': user_data['name'],
        'email': user_data['email']
    }
    users.append(user)
    with open("./users.json", "w") as f:
        json.dump(users, f)
    return redirect(url_for('get_users'), code=302)


@app.route('/users/new')
def users_new():
    user = {
        'name': '',
        'email': ''
    }
    errors = {}

    return render_template(
        'users/new.html',
        user=user,
        errors=errors
    )


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


def validate(user):
    errors = {}
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors
