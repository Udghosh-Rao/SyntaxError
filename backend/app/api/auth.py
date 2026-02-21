"""
Authentication Blueprint
Endpoints: POST /api/register, POST /api/login, GET /api/me, PUT /api/me
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..extensions import db
from ..models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user (user or organizer role only — admin seeded directly)."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required = ['name', 'email', 'password', 'role']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    # Prevent public admin registration
    if data.get('role') == 'admin':
        return jsonify({'error': 'Admin accounts cannot be registered publicly'}), 403

    if data.get('role') not in ('user', 'organizer'):
        return jsonify({'error': 'Role must be user or organizer'}), 400

    # Check existing email
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    user = User(
        name=data['name'],
        email=data['email'],
        role=data['role'],
        city=data.get('city'),
        budget_preference=data.get('budget_preference', 'mid'),
        preferred_sports=data.get('preferred_sports', []),
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    return jsonify({
        'message': 'Registration successful',
        'token': token,
        'user_id': user.id,
        'role': user.role,
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT with role claim."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user_id': user.id,
        'role': user.role,
        'name': user.name,
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    """Return authenticated user's profile."""
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200


@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_me():
    """Update authenticated user's profile (city, budget, sports prefs)."""
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}

    if 'city' in data:
        user.city = data['city']
    if 'budget_preference' in data:
        if data['budget_preference'] not in ('cheap', 'mid', 'premium'):
            return jsonify({'error': 'budget_preference must be cheap, mid, or premium'}), 400
        user.budget_preference = data['budget_preference']
    if 'preferred_sports' in data:
        user.preferred_sports = data['preferred_sports']
    if 'name' in data:
        user.name = data['name']

    db.session.commit()
    return jsonify({'message': 'Profile updated', 'user': user.to_dict()}), 200
