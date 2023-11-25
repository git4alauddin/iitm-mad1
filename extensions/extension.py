# imports
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restx import Api
from flask_migrate import Migrate

# initializations
db = SQLAlchemy()
bcrypt = Bcrypt()
api = Api()
migrate = Migrate()

login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    from models.user_model import User, Admin 
    admin = Admin.query.get(str(user_id))
    if admin is not None:
        return admin 
    return User.query.get(str(user_id))