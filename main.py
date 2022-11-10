from re import I
from flask import request, make_response, redirect, render_template, session, url_for, flash
from app import create_app

app=create_app()

@app.route('/')
def index():
    user_ip = request.remote_addr
    return render_template('index.html', user_ip=user_ip)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)