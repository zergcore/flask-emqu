from flask import render_template, session, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from app.forms import LoginForm
from . import auth
from app.models import db, get_user, User

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
    if signup_form.validate_on_submit():
        email= signup_form.email.data
        password= signup_form.password.data
        user_row=get_user(email)
        if user_row:
            flash('El nombre de usuario ya existe')
            return redirect(url_for('auth.signup'))
        else:
            new_user= User(email= email, password= generate_password_hash(password, method= 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Bienvenido(a)')
            return redirect(url_for('hello'))
        
    return render_template('signup.html', **context)
