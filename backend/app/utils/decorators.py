"""
Role-based access control decorators.
Implements role_required(role) as per Agent Rule #4.
Returns HTTP 403 if the JWT role claim doesn't match.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt


def role_required(*allowed_roles):
    """
    Decorator factory that enforces role-based access.
    Usage: @role_required('admin') or @role_required('user', 'organizer')
    Must be applied AFTER @jwt_required().
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role', '')
            if user_role not in allowed_roles:
                return jsonify({
                    'error': 'Forbidden: insufficient role',
                    'required': list(allowed_roles),
                    'your_role': user_role,
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
