# imports
import uuid
from flask_login import UserMixin
from extensions.extension import db

def generate_uuid():
    return str(uuid.uuid4())

# model user
class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')

    # remove it
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.role = 'user'

# model admin
# set the uuid thing as in user
class Admin(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='admin')