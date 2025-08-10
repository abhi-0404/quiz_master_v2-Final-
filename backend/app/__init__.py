from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_caching import Cache
from celery import Celery
import os
from dotenv import load_dotenv
from datetime import date

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
cache = Cache()
celery = Celery()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # --- FIX: Enable CORS for the application ---
    # This must be done right after the app is created and allows
    # your frontend (localhost:8080) to communicate with the backend.
    CORS(app)
    
    # --- Configuration ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///quiz_master.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # For development
    
    # Redis configuration
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Mail configuration
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT') or 587)
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    
    # Celery configuration
    app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/1'
    app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/2'
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    
    # Configure Celery
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.user import user_bp
    from app.routes.quiz import quiz_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        from app.models.user import User
        admin = User.query.filter_by(email=os.environ.get('ADMIN_EMAIL', 'admin@quizmaster.com')).first()
        if not admin:
            admin = User(
                email=os.environ.get('ADMIN_EMAIL', 'admin@quizmaster.com'),
                full_name='Administrator',
                role='admin',
                qualification='System Admin',
                dob=date(1990, 1, 1)
            )
            admin.set_password(os.environ.get('ADMIN_PASSWORD', 'admin123'))
            db.session.add(admin)
            db.session.commit()
    
    return app
