from flask import Flask, request, redirect, render_template

app = Flask('resourse')

@app.route('/')
def base_view():
    return '''
<a href='/auth/login'>login</a>
<a href='/auth/register'>register</a>
<a href='/auth/logout'>logout</a>
''', 200

@app.route('/auth/register')
def register_view():
    return '', 200

@app.route('/auth/login')
def login_view():
    return '', 200

@app.route('/auth/logout')
def logout_view():
    return '', 200

@app.route('/app')
def app_view():
    return '', 200

