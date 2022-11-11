from flask import render_template, session, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash,check_password_hash

from app.forms import LoginForm
from . import auth
from app.models import db, get_user, User

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form=LoginForm()
    context = {
        'login_form': login_form
    }
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user_row=get_user(email)
        if user_row:
            password_from_db=user_row.password
            if check_password_hash(password_from_db, password):
                login_user(user_row)
                flash('Welcome again!','success')
                return redirect((url_for('dashboard')))
            else:
                flash("Info doesn't match", 'warning')
        else:
            flash("User doesn't exist, please try again, you may have some typo issues", 'warning')

        return redirect(url_for('login.html'))

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
            flash('The email is already registered in our database.', 'warning')
        else:
            new_user= User(email= email, password= generate_password_hash(password, method= 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Welcome to our platorm!', 'success')
            return redirect(url_for('dashboard'))
        
    return render_template('signup.html', **context)

@auth.route('/logout',  methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
