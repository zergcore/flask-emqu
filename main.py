from re import I
from flask import request, make_response, redirect, render_template, session, url_for, flash
from app import create_app
from app.models import get_users
from flask_login import login_required, logout_user

app=create_app()

@app.route('/')
def index():
    user_ip = request.remote_addr
    users=get_users()
    context={
        'user_ip':user_ip,
        'users':users
    }
    return render_template('index.html', **context)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

