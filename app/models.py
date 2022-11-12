from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime as dt

db = SQLAlchemy()

class DeviceResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    response = db.Column(db.Integer, nullable=False)
    avg_latency = db.Column(db.Float, nullable=False)
    min_latency = db.Column(db.Float, nullable=False)
    max_latency = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship('Device', backref=db.backref('responses', lazy=True))
    

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    ipv4 = db.Column(db.String(16), nullable=False)
    status = db.Column(db.Boolean, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('devices', lazy=True))

class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key= True, autoincrement= True)
    email= db.Column(db.String(30), unique= True, nullable= False)
    password= db.Column(db.String(80), nullable= False)


def get_user(email):
    user= User.query.filter_by(email=email).first()
    return user

def get_users():
    users=User.query.order_by(User.id).all()
    return users

def get_user_id(email):
    current_user=get_user(email)
    return current_user.id

def get_user_devices(email):
    user=get_user(email)
    return user.devices

def put_device(email, name, ipv4):
    user=get_user(email)
    d=Device(name=name, ipv4=ipv4)
    user.devices.append(d)
    db.session.add(user)
    db.session.commit()

def delete_device(user_id, device_id):
    user=User.query.filter_by(id=user_id).first()
    device=Device.query.with_parent(user).filter_by(id=device_id).first()
    db.session.delete(device)
    db.session.commit()

def test_device(device_id, device_status):
    device=Device.query.filter_by(id=device_id).first()
    device.status = device_status
    db.session.commit()

def get_device(device_id):
    device=Device.query.filter_by(id=device_id).first()
    return device

def get_device_responses(device_id):
    device=get_device(device_id)
    return device.responses

def get_devices_responses():
    responses=DeviceResponse.query\
        .join(Device, DeviceResponse.device_id==Device.id)\
        .add_columns(Device.name, Device.ipv4, DeviceResponse.avg_latency, DeviceResponse.min_latency, DeviceResponse.max_latency,DeviceResponse.response, DeviceResponse.status, DeviceResponse.created_at)\
        .order_by(DeviceResponse.created_at.desc())\
        .all()
    return responses

def get_last_device_responses(device_id):
    #device=get_device(device_id)
    #responses=device.responses.order_by(responses.created_at.desc()).limit(3)

    responses=DeviceResponse.query\
        .join(Device, DeviceResponse.device_id==Device.id)\
        .add_columns(Device.name, Device.ipv4, DeviceResponse.avg_latency, DeviceResponse.min_latency, DeviceResponse.max_latency,DeviceResponse.response, DeviceResponse.status, DeviceResponse.created_at)\
        .order_by(DeviceResponse.created_at.desc())\
        .filter_by(Device.id==device_id)\
        .limit(3)
    return responses


def put_response(device_id, response, avg, min, max, status):
    device=get_device(device_id)
    response=DeviceResponse(response=response, avg_latency=avg, min_latency=min, max_latency=max, status=status)
    device.responses.append(response)
    db.session.add(device)
    db.session.commit()

def get_active_devices():
    active=Device.query.filter_by(status=True).all()
    return active

def get_inactive_devices():
    inactive=Device.query.filter_by(status=False).all()
    return inactive

def get_active_responses_per_device():
    devices=Device.query.all()
    active_responses={}
    for device in devices:
        active=db.session.query(DeviceResponse).filter_by(device_id=device.id).filter_by(status=True).count()
        active_responses[device.name]=active
    return active_responses