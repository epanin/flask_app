from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages, session
import json, uuid, lesson_ws.data.users as users_rep

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def root():
    if session.get('email') is None:
        errors = {}
        credentials = {}
        return render_template('users/login.html',
                            errors=errors,
                            credentials=credentials)
    else:
        return redirect(url_for('users_get'), code=302)

@app.get('/login')
def login():
    errors = {}
    credential_email = request.args.get('email')
    if errors:
        return render_template('users/login.html',
                           errors=errors,
                           credentials=credential_email)
    session['email'] = credential_email
    return redirect(url_for('users_get'), code=302)

# Read

@app.get('/users')
def users_get():
    users = users_rep.get_users()
    users_list = [info for info in users.values()]
    messages = get_flashed_messages(with_categories=True)
    credential_email = session.get('email')
    return render_template(
        'users/index.html',
        users=users_list,
        messages=messages, 
        credential_email=credential_email
    )

@app.get('/user/<id>')
def user_get(id):
    user_info = users_rep.find_user(id)
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
    users_rep.save_user(user)
    flash('New user created!', 'success')    
    return redirect(url_for('users_get'), code=302)

# Update
   
@app.route('/user/<id>/edit')
def user_edit(id):
    user_info = users_rep.find_user(id)
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
    user_info = users_rep.find_user(id)
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
    users_rep.save_user(user_info)
    flash('User has been updated!', 'success')    
    return redirect(url_for('users_get'), code=302)

# Delete

@app.route('/user/<id>/delete')
def user_delete(id):
    user_info = users_rep.find_user(id)
    if not user_info:
        return 'Page not found', 404
    return render_template(
        'users/delete.html',
        user=user_info
        )

@app.post('/users/<id>/delete')
def user_destroy(id):
    users_rep.destroy(id)
    flash('User has been deleted', 'success')
    return redirect(url_for('users_get'))