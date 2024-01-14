from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    print(request.headers)
    return 'Welcome to Flask\n'

@app.get('/users/<id>/')
def users_get(id):
    return render_template(
        'test.html', 
        name=id
        )

@app.post('/users')
def users_post():
    return 'Users\n', 302

@app.route('/html/')
def html():
    return render_template('/index.html')

@app.route('/not_found/')
def not_found():
    return 'OOps', 404

@app.route('/courses/<id>')
def course(id):
    return f'Course id: {id}'

