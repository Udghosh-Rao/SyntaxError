from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User

def role_required(*required_roles):
    """
    Custom decorator to protect endpoints by role as per Spec 4.
    If the user's role is not in required_roles, return HTTP 403 Forbidden.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or user.role not in required_roles:
                return {'message': 'Forbidden: Insufficient permissions'}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
