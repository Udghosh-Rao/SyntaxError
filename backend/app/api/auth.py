from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from app.extensions import db
from app.models.user import User, generate_referral_code
import os
import requests as http_requests

auth_ns = Namespace('auth', description='Authentication operations')

@auth_ns.route('/register')
class Register(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(email=data.get('email')).first():
            return {'message': 'Email already exists'}, 400
        role = data.get('role', 'user')
        if role == 'admin':
            return {'message': 'Admin cannot be registered publicly'}, 403
        referred_by_id = None
        incoming_code = (data.get('referral_code') or '').strip().upper()
        if incoming_code:
            referrer = User.query.filter_by(referral_code=incoming_code).first()
            if not referrer:
                return {'message': 'Invalid referral code'}, 400
            referred_by_id = referrer.id
        new_code = generate_referral_code()
        while User.query.filter_by(referral_code=new_code).first():
            new_code = generate_referral_code()
        user = User(
            name=data.get('name', data.get('username')),
            email=data.get('email'),
            role=role,
            city=data.get('city'),
            budget_preference=data.get('budget_preference', 'mid'),
            preferred_sports=data.get('preferred_sports', []),
            referral_code=new_code,
            referred_by_id=referred_by_id,
        )
        user.set_password(data.get('password'))
        try:
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={'role': user.role},
                expires_delta=timedelta(days=30)
            )
            return {'user_id': user.id, 'access_token': access_token, 'referral_code': user.referral_code}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error creating user: {str(e)}'}, 400


@auth_ns.route('/login')
class Login(Resource):
    def post(self):
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
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    def put(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        data = request.get_json()
        user.name = data.get('name', user.name)
        user.city = data.get('city', user.city)
        user.budget_preference = data.get('budget_preference', user.budget_preference)
        user.preferred_sports = data.get('preferred_sports', user.preferred_sports)
        db.session.commit()
        return user.to_dict(), 200


@auth_ns.route('/oauth/google')
class GoogleOAuth(Resource):
    def post(self):
        """
        Step 1 of Google OAuth.
        - Existing user  → returns access_token + is_new_user: false  → redirect immediately
        - New user       → creates stub account, returns temp token + is_new_user: true
                           → frontend shows onboarding form
        """
        data = request.get_json()
        id_token_value = data.get('id_token')
        if not id_token_value:
            return {'message': 'id_token is required'}, 400

        google_response = http_requests.get(
            f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token_value}',
            timeout=10
        )
        if google_response.status_code != 200:
            return {'message': 'Invalid Google token'}, 401

        google_data = google_response.json()
        client_id = os.getenv('GOOGLE_CLIENT_ID', '')
        if client_id and google_data.get('aud') != client_id:
            return {'message': 'Token audience mismatch'}, 401

        email = google_data.get('email')
        name  = google_data.get('name', email)
        if not email:
            return {'message': 'Could not retrieve email from Google'}, 400

        user = User.query.filter_by(email=email).first()

        # ── Existing user: sign in normally ──────────────────────────────────
        if user:
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={'role': user.role},
                expires_delta=timedelta(days=30)
            )
            return {
                'is_new_user':    False,
                'access_token':   access_token,
                'role':           user.role,
                'user_id':        user.id,
                'name':           user.name,
                'email':          user.email,
            }, 200

        # ── New user: create stub, return temp token for onboarding ──────────
        new_code = generate_referral_code()
        while User.query.filter_by(referral_code=new_code).first():
            new_code = generate_referral_code()

        user = User(
            name=name,
            email=email,
            role='user',               # default; updated in /complete step
            budget_preference='mid',
            preferred_sports=[],
            referral_code=new_code,
        )
        user.set_password(os.urandom(24).hex())
        db.session.add(user)
        db.session.commit()

        # Temporary token scoped to onboarding (short-lived: 15 min)
        temp_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role, 'onboarding': True},
            expires_delta=timedelta(minutes=15)
        )
        return {
            'is_new_user':  True,
            'temp_token':   temp_token,
            'user_id':      user.id,
            'name':         user.name,
            'email':        user.email,
        }, 200


@auth_ns.route('/oauth/google/complete')
class GoogleOAuthComplete(Resource):
    @jwt_required()
    def post(self):
        """
        Step 2 of Google OAuth — completes the new-user onboarding.
        Expects: role, city, preferred_sports (for users)
        Returns: final access_token with correct role.
        """
        user_id = int(get_jwt_identity())
        user    = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        data = request.get_json()
        role = data.get('role', 'user')
        if role == 'admin':
            return {'message': 'Cannot assign admin role'}, 403

        user.role             = role
        user.city             = data.get('city', '')
        user.preferred_sports = data.get('preferred_sports', [])
        user.budget_preference = data.get('budget_preference', 'mid')

        db.session.commit()

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role},
            expires_delta=timedelta(days=30)
        )
        return {
            'access_token': access_token,
            'role':         user.role,
            'user_id':      user.id,
            'name':         user.name,
            'email':        user.email,
        }, 200


@auth_ns.route('/my-referrals')
class MyReferrals(Resource):
    @jwt_required()
    def get(self):
        """
        Returns referral stats for the current user.

        Counts TWO types of referrals:
          1. Account referrals  — users who signed up using this code
             (stored in users.referred_by_id)
          2. Event referrals    — registrations where this code was used
             at checkout (stored in wallet_transactions type='referral_bonus')
        Total shown is the union of both.
        """
        user_id = int(get_jwt_identity())
        user    = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        # ── Account-level referrals (signed up via code) ──────────────────────
        account_referrals = [
            {
                'id':        r.id,
                'name':      r.name,
                'type':      'account',
                'joined_at': r.created_at.isoformat() if r.created_at else None,
            }
            for r in user.referrals
        ]

        # ── Event-level referrals (used code at checkout) ─────────────────────
        # Count wallet_transactions of type referral_bonus belonging to this user.
        # These are created in payments/verify whenever someone uses this user's
        # referral code at event checkout (distinct from account-signup referrals).
        from app.models.wallet import Wallet, WalletTransaction
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        event_bonus_txns = []
        if wallet:
            event_bonus_txns = WalletTransaction.query.filter_by(
                wallet_id=wallet.id,
                type='referral_bonus'
            ).order_by(WalletTransaction.created_at.desc()).all()

        event_referrals = [
            {
                'id':        f'evt_{txn.id}',
                'name':      txn.description,
                'type':      'event',
                'joined_at': txn.created_at.isoformat() if txn.created_at else None,
                'bonus':     txn.amount,
            }
            for txn in event_bonus_txns
        ]

        all_referrals   = account_referrals + event_referrals
        total_referrals = len(all_referrals)

        return {
            'referral_code':   user.referral_code,
            'total_referrals': total_referrals,
            'referrals':       all_referrals,
        }, 200