from flask import Flask, request, render_template, redirect
import json, uuid

app = Flask(__name__)

@app.route('/')
def hello_world():
    print(request.headers)
    return 'Welcome to Flask\n'

@app.get('/users')
def users_get():
    return render_template(
        'test.html'
        )


@app.route('/html/')
def html():
    return render_template('/index.html')

@app.route('/not_found/')
def not_found():
    return 'OOps', 404

@app.route('/courses/<id>')
def course(id):
    return f'Course id: {id}'

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
    id = 1
    user['id'] = id
    with open('users.txt', 'a', encoding='utf-8') as f:
        json.dump(user, f) 
    return redirect('/users', code=302)

def validate(user_data):
    errors = {}
#     if not user['name']:
#         errors['name'] = "Can't be blank"
#
#     # ...
#
#     return errors
    return errors    