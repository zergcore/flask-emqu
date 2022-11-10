from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__= 'Users'
    id= db.Column(db.Integer, primary_key= True, autoincrement= True)
    email= db.Column(db.String(20), unique= True, nullable= False)
    password= db.Column(db.String(50), nullable= False)

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