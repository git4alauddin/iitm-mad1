# imports
import uuid
from flask_login import UserMixin
from extensions.extension import db

# form defaults
def generate_uuid():
    return str(uuid.uuid4())

# user
class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')

# admin
class Admin(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='admin')

# flagged_creators
class FlaggedCreator(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    admin_id = db.Column(db.String(36), db.ForeignKey('admin.id'), nullable=False)