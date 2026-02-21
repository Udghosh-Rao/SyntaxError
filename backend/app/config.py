"""
Configuration classes for Development and Production environments.
All secrets loaded from environment variables — never hardcoded.
"""
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens don't expire during dev

    # Razorpay
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')
    PLATFORM_FEE_PERCENT = float(os.getenv('PLATFORM_FEE', '0.15'))

    # Algolia
    ALGOLIA_APP_ID = os.getenv('ALGOLIA_APP_ID', '')
    ALGOLIA_API_KEY = os.getenv('ALGOLIA_API_KEY', '')
    ALGOLIA_INDEX = os.getenv('ALGOLIA_INDEX', 'events')

    # OpenAI / GenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')

    # Price tier thresholds (configurable)
    PRICE_TIER_CHEAP_MAX = int(os.getenv('PRICE_TIER_CHEAP_MAX', '500'))
    PRICE_TIER_MID_MAX = int(os.getenv('PRICE_TIER_MID_MAX', '2000'))


class DevelopmentConfig(Config):
    """Development configuration using SQLite."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(BASE_DIR, '..', 'sports_dev.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """Production configuration using PostgreSQL."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours in production
