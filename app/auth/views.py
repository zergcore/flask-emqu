from flask import render_template, session, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from app.forms import LoginForm
from . import auth

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form=LoginForm()
    context = {
        'login_form': login_form
    }
    return render_template('login.html', **context)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form=LoginForm()
    context={
        'signup_form':signup_form
    }
    return render_template('signup.html', **context)
