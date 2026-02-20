from flask import Flask
from app.extensions import db, jwt, cors, migrate, jwt
from app.api import auth, events, registrations, payments, chatbot, organizer, admin

def create_app(config=None):
    app = Flask(__name__)
    
    if config:
        app.config.from_object(config)
    else:
        from app.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    migrate.init_app(app, db)
jwt.init_app(app)
    
    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.events import events_bp
    from app.api.registrations import reg_bp
    from app.api.payments import pay_bp
    from app.api.chatbot import chat_bp
    from app.api.organizer import org_bp
    from app.api.admin import admin_bp
from app.api.auth import auth_bp
from app.api.admin import admin_bp
    
    for bp in [auth_bp, events_bp, reg_bp, pay_bp, chat_bp, org_bp, , auth_bp, admin_bpadmin_bp]:
        app.register_blueprint(bp, url_prefix='/api')
    
    return app
