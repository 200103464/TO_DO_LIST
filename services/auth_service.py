from models.user_model import User
from app import db

def register_user(email, password):
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get_or_404(user_id)
