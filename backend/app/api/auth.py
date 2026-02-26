from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from app.extensions import db
from app.models.user import User

auth_ns = Namespace('auth', description='Authentication operations')

@auth_ns.route('/register')
class Register(Resource):
    def post(self):
        """Register a new user (Spec 6.1)"""
        data = request.get_json()
        
        if User.query.filter_by(email=data.get('email')).first():
            return {'message': 'Email already exists'}, 400
            
        role = data.get('role', 'user')
        if role == 'admin':
            return {'message': 'Admin cannot be registered publicly'}, 403

        user = User(
            name=data.get('name', data.get('username')),  # support both for legacy compat
            email=data.get('email'),
            role=role,
            city=data.get('city'),
            budget_preference=data.get('budget_preference', 'mid'),
            preferred_sports=data.get('preferred_sports', [])
        )
        user.set_password(data.get('password'))
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Additional claim 'role' added for Vue router
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={'role': user.role},
                expires_delta=timedelta(days=30)
            )
            return {'user_id': user.id, 'access_token': access_token}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error creating user: {str(e)}'}, 400

@auth_ns.route('/login')
class Login(Resource):
    def post(self):
        """Authenticate user (Spec 6.1)"""
        data = request.get_json()
        
        user = User.query.filter_by(email=data.get('email')).first()
        if not user or not user.check_password(data.get('password')):
            return {'message': 'Invalid credentials'}, 401
            
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role},
            expires_delta=timedelta(days=30)
        )
        return {'access_token': access_token, 'role': user.role}, 200

@auth_ns.route('/me')
class Me(Resource):
    @jwt_required()
    def get(self):
        """Get profile (Spec 6.1)"""
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    def put(self):
        """Update profile (Spec 6.1)"""
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        data = request.get_json()
        
        user.city = data.get('city', user.city)
        user.budget_preference = data.get('budget_preference', user.budget_preference)
        user.preferred_sports = data.get('preferred_sports', user.preferred_sports)
        
        db.session.commit()
        return user.to_dict(), 200
