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
    # Consultar una persona
    user= User.query.filter_by(email=email).first()
    return user

def get_users():
    users=User.query.order_by(User.id).all()
    return users

def get_user_id(email):
    current_user=get_user(email)
    return current_user.id