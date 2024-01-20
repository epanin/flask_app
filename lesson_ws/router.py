from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
import json, uuid, lesson_ws.data.users as users_rep

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def hello_world():
    print(request.headers)
    return 'Welcome to Flask\n'

# Read

@app.get('/users')
def users():
    users_list = users_rep.get_users()
    return render_template(
        'users/index.html',
        users=users_list
    )

@app.get('/user/<id>')
def user(id):
    messages = get_flashed_messages(with_categories=True)
    user_info = users_rep.find_user(id)
    if not user_info:
        pass
    return render_template(
        'users/show.html',
        user=user_info, 
        messages=messages
        )


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
    errors = {}#validate(user)
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


   

