"""
Application factory for Sports Event Management MVP.
"""
from flask import Flask
from .config import DevelopmentConfig, ProductionConfig
from .extensions import db, jwt, cors, migrate
import os


def create_app(config_name=None):
    app = Flask(__name__)

    # Load config
    env = config_name or os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    migrate.init_app(app, db)

    # Register blueprints
    from .api.auth import auth_bp
    from .api.events import events_bp
    from .api.registrations import registrations_bp
    from .api.payments import payments_bp
    from .api.chatbot import chatbot_bp
    from .api.organizer import organizer_bp
    from .api.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(events_bp, url_prefix='/api')
    app.register_blueprint(registrations_bp, url_prefix='/api')
    app.register_blueprint(payments_bp, url_prefix='/api')
    app.register_blueprint(chatbot_bp, url_prefix='/api')
    app.register_blueprint(organizer_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')

    # Health check
    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'message': 'Sports Event Management API is running'}, 200

    return app
