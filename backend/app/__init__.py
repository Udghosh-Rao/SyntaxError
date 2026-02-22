from flask import Flask
from app.extensions import db, jwt, cors, migrate


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
    
    # Register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp)
    
    return app
