from flask import Flask, request, make_response, render_template, redirect, url_for, flash, get_flashed_messages
import json, uuid, lesson_ws.data.users as users_rep

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def hello_world():
    print(request.headers)
    return 'Welcome to Flask\n'

# Read

@app.get('/users')
def users_get():
    #users = users_rep.get_users()
    #users_list = [info for info in users.values()]
    users_dict: dict = json.loads(request.cookies.get('users', json.dumps({})))
    users_list = list(users_dict.values())
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'users/index.html',
        users=users_list,
        messages=messages
    )

@app.get('/user/<id>')
def user_get(id):
    #user_info = users_rep.find_user(id)
    users_dict: dict = json.loads(request.cookies.get('users', json.dumps({})))
    user_info = users_dict.get(id)
    if not user_info:
        return 'Page not found', 404
    return render_template(
        'users/show.html',
        user=user_info
        )

# Create

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
    errors = users_rep.validate(user)
    if errors:
        return render_template(
            'users/new.html',
            user=user, 
            errors=errors
        ), 422
    #users_rep.save_user(user)
    users_dict: dict = json.loads(request.cookies.get('users', json.dumps({})))
    id = str(uuid.uuid4())
    user['id'] = id
    users_dict[id] = user
    response = make_response(redirect(url_for('users_get'), code=302))
    response.set_cookie('users', json.dumps(users_dict))
    flash('New user created!', 'success')    
    return response

# Update
   
@app.route('/user/<id>/edit')
def user_edit(id):
    users_dict: dict = json.loads(request.cookies.get('users', json.dumps({})))
    user_info = users_dict.get(id)
    errors = {}
    if not user_info:
        return 'Page not found', 404
    return render_template(
        'users/edit.html',
        errors=errors,
        user=user_info
        )

@app.post('/user/<id>/patch')
def user_patch(id):
    users_dict: dict = json.loads(request.cookies.get('users', json.dumps({})))
    user_info = users_dict.get(id)
    user_data = request.form.to_dict()
    errors = users_rep.validate(user_data)
    if errors:
        render_template(
            'users/edit.html',
        errors=errors,
        user=user_info
        ), 422
    user_info['name'] = user_data['name']
    user_info['email'] = user_data['email']
    #users_rep.save_user(user_info)
    response = make_response(redirect(url_for('users_get'), code=302))
    response.set_cookie('users', json.dumps(users_dict))
    flash('User has been updated!', 'success')    
    return response

# Delete

@app.route('/user/<id>/delete')
def user_delete(id):
    #user_info = users_rep.find_user(id)
    users_dict: dict = json.loads(request.cookies.get('users', json.dumps({})))
    user_info = users_dict.get(id)
    if not user_info:
        return 'Page not found', 404
    return render_template(
        'users/delete.html',
        user=user_info
        )

@app.post('/users/<id>/delete')
def user_destroy(id):
    #users_rep.destroy(id)
    users_dict: dict = json.loads(request.cookies.get('users', json.dumps({})))
    users_dict.pop(id)
    response = make_response(redirect(url_for('users_get'), code=302))
    response.set_cookie('users', json.dumps(users_dict))
    flash('User has been deleted', 'success')
    return response