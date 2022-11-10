from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__= 'Users'
    def __init__(self, email, password):
        self.email= email
        self.password= password
    
    id= db.Column(db.Integer, primary_key= True, autoincrement= True)
    email= db.Column(db.String(20), unique= True, nullable= False)
    password= db.Column(db.String(50), nullable= False)

def get_user(email):
    # Consultar una persona
    usuario= User.query.filter_by(email=email).first()
    return usuario

def get_users():
    users=User.query.order_by(User.id).all()
    return users