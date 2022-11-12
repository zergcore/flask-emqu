from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Device(db.Model):
    # __tablename__ = 'Devices'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    ipv4 = db.Column(db.String(16), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('devices', lazy=True))

class User(db.Model, UserMixin):
    # __tablename__= 'Users'
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
    devices=len(Device.query.all())+1
    d=Device(id=devices,name=name, ipv4=ipv4, status=True)
    user.devices.append(d)
    db.session.add(user)
    db.session.commit()

def delete_device(user_id, device_id):
    user=User.query.filter_by(id=user_id).first()
    device=Device.query.with_parent(user).filter_by(id=device_id).first()
    db.session.delete(device)
    db.session.commit()

def test_device(device_id, device_status):
    test= not bool(device_status)
    device=Device.query.filter_by(id=device_id).first()
    device.status = test
    db.session.commit()