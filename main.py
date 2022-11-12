from re import I
from flask import request, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user
from app import create_app
from app.models import get_users,get_user_devices, put_device, delete_device, test_device, get_devices_responses, get_device, put_response, get_device_responses, get_active_devices, get_inactive_devices, get_active_responses_per_device
from app.forms import DeviceForm, DeleteDeviceForm, TestDeviceForm
from app.utils import verify_ping, ping_host

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
        flash('Your device was created successfully!', 'success')
        return redirect(url_for('devices'))  

    return render_template('devices.html', **context)

@app.route('/devices/delete/<device_id>', methods=['POST'])
def delete(device_id):
    user_id = current_user.id
    responses=get_device_responses(device_id)
    if len(responses):
        flash('You have done tests to this device, now you cannot delete it', 'danger')
        return redirect(url_for('devices'))
    else:
        delete_device(user_id=user_id, device_id=device_id)

    return redirect(url_for('devices'))

@app.route('/devices/test/<device_id>', methods=['POST'])
async def test(device_id):

    device=get_device(device_id)
    data = await verify_ping(device.ipv4)
    data.update(await ping_host(device.ipv4))
    status=data['response']==0 
    test_device(device_id, status)
    put_response(device_id,data['response'],data['avg_latency'],data['min_latency'],data['max_latency'],status)
    flash('Test made successfully, please go to stadistics so you can see the details', 'success')
    return redirect(url_for('devices'))

@app.route('/stadistics', methods=['GET', 'POST'])
@login_required
def stadistics():
    user_id=session['user_id']
    responses=get_devices_responses()
    data_active_inactive=[len(get_active_devices()), len(get_inactive_devices())]
    data_active_responses=get_active_responses_per_device()
    active_devices=data_active_responses.keys()
    active_data=data_active_responses.values()
    context={
        'user_id':user_id,
        'responses':responses,
        'data_active_inactive':data_active_inactive,
        'active_devices': active_devices,
        'active_data': active_data
    }

    return render_template('stadistics.html', **context)