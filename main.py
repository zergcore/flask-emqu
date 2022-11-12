from re import I
from flask import request, make_response, redirect, render_template, session, url_for, flash
from app import create_app
from app.models import get_users,get_devices, put_device
from flask_login import login_required, logout_user
from app.forms import DeviceForm

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
    user_id=session['user_id']
    context={
        'user_id':user_id
    }
    return render_template('dashboard.html', **context)

@app.route('/devices', methods=['GET', 'POST'])
@login_required
def devices():
    user_id=session['user_id']
    device_form=DeviceForm()
    devices=get_devices(user_id)
    context={
        'user_id':user_id,
        'devices':devices,
        'device_form':device_form
    }

    if device_form.validate_on_submit():
        put_device(email=user_id, name=device_form.name.data, ipv4=device_form.ipv4.data)
        flash('Your task was created successfully!', 'success')
        return redirect(url_for('devices'))  

    return render_template('devices.html', **context)
