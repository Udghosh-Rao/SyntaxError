from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash
from app.extensions import db, jwt
from app.models.user import User
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_ns = Namespace('auth', description='Authentication operations')

# Models for API documentation
user_model = auth_ns.model('User', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(enum=['user', 'organizer', 'admin'], default='user')
})

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(user_model)
    @auth_ns.response(201, 'User created successfully')
    @auth_ns.response(400, 'Username or email already exists')
    def post(self):
        """Register a new user"""
        data = request.get_json()
        
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists'}, 400
        
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'user')
        )
        user.set_password(data['password'])
        
        try:
            db.session.add(user)
            db.session.commit()
            
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=30))
            
            return {
                'message': 'User created successfully',
                'user': user.to_dict(),
                'access_token': access_token
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error creating user: {str(e)}'}, 400

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Login successful')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """Login user"""
        data = request.get_json()
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return {'message': 'Invalid username or password'}, 401
        
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=30))
        
        return {
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token
        }, 200

@auth_ns.route('/profile')
class Profile(Resource):
    @jwt_required()
    @auth_ns.response(200, 'Profile retrieved successfully')
    @auth_ns.response(401, 'Unauthorized')
    def get(self):
        """Get current user profile"""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return {'message': 'User not found'}, 404
        
        return {'user': user.to_dict()}, 200
