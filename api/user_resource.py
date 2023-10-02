from flask_restx import Resource, Namespace
from models.user_model import User
from flask_login import current_user
from api.api_models import user_model, user_input_model
from decorators.role_decorator import admin_required, user_required
from extensions.extension import db

ns_user = Namespace('user')

@ns_user.route('/users/<string:id>')
class UserApi(Resource):
    @ns_user.marshal_with(user_model)
    def get(self, id):
        user = User.query.get(id)
        return user
    
    @ns_user.expect(user_input_model)
    @ns_user.marshal_with(user_model)
    def put(self,id):
        user = User.query.get(id)
        user.role = 'creator'
        db.session.commit()
        return user 
    
    @ns_user.marshal_with(user_model)
    def delete(self, id):
        user = User.query.get(id)
        user.role = 'user'
        db.session.commit()
        return user



ns_users = Namespace('users')

@ns_users.route('/users')
class UsersListApi(Resource):
    @ns_users.marshal_with(user_model)
    def get(self):
        user = User.query.all()
        return user


