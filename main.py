from re import I
from flask import request, make_response, redirect, render_template, session, url_for, flash, jsonify
from app import create_app
from app.models import get_users,get_user_devices, put_device, delete_device, test_device
from flask_login import login_required, current_user
from app.forms import DeviceForm, DeleteDeviceForm, TestDeviceForm
from app.utils import verify_ping

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
    delete_form=DeleteDeviceForm()
    test_form=TestDeviceForm()
    devices=get_user_devices(user_id)
    context={
        'user_id':user_id,
        'devices':devices,
        'device_form':device_form,
        'delete_form':delete_form,
        'test_form':test_form
    }

    if device_form.validate_on_submit():
        put_device(email=user_id, name=device_form.name.data, ipv4=device_form.ipv4.data)
        flash('Your task was created successfully!', 'success')
        return redirect(url_for('devices'))  

    return render_template('devices.html', **context)

@app.route('/devices/delete/<device_id>', methods=['POST'])
def delete(device_id):
    user_id = current_user.id
    delete_device(user_id=user_id, device_id=device_id)

    return redirect(url_for('devices'))

@app.route('/devices/test/<device_id>/<int:status>', methods=['POST'])
def test(device_id, status):

    test_device(device_id=device_id, device_status=status)

    return redirect(url_for('devices'))

@app.route("/devices/test/<device_ipv4>", methods=['POST'])
async def test_ip(device_ipv4):
    data = await verify_ping(device_ipv4)
    return jsonify(data)