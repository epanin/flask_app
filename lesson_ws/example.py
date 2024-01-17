from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
import json, uuid

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def hello_world():
    print(request.headers)
    return 'Welcome to Flask\n'


@app.get('/users/<name>')
def users_get(name):
    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'test.html',
        name=name, 
        messages=messages
        )


@app.route('/html/')
def html():
    return render_template('index.html')


@app.route('/users/new')
def users_new():
    user = {'name': '', 'email': ''}
    errors = {}

    return render_template(
        'users/new.html',
        user=user, 
        errors=errors,
    )


@app.post('/users')
def users_post():
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template(
            'users/new.html',
            user=user, 
            errors=errors
        ), 422
    id = str(uuid.uuid4())
    user['id'] = id
    flash('New user created!', 'success')
    with open('lesson_ws/data/users.txt', 'a', encoding='utf-8') as f:
        json.dump(user, f)
        f.write('\n') 
    return redirect(url_for('users_get', name=user.get('name')), code=302)


def validate(user_data):
    errors = {}
    if not user_data['name']:
        errors['name'] = "Can't be blank"

    return errors    