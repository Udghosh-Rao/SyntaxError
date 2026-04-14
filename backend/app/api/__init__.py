from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    api_bp,
    version='1.0',
    title='Sports Event Management API',
    description='API for Sports Event Management MVP',
    doc='/docs'
)

from .auth          import auth_ns
from .events        import events_ns
from .registrations import registrations_ns
from .payments      import payments_ns
from .chatbot       import chatbot_ns
from .admin         import admin_ns
from .organizer     import organizer_ns
from .wallet        import wallet_ns

api.add_namespace(auth_ns,          path='/auth')
api.add_namespace(events_ns,        path='/events')
api.add_namespace(registrations_ns, path='/registrations')
api.add_namespace(payments_ns,      path='/payments')
api.add_namespace(chatbot_ns,       path='/chatbot')
api.add_namespace(admin_ns,         path='/admin')
api.add_namespace(organizer_ns,     path='/organizer')
api.add_namespace(wallet_ns,        path='/wallet')

__all__ = ['api_bp', 'api']