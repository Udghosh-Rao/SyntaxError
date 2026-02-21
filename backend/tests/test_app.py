"""Basic smoke tests for the Flask application."""
import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


def test_register_user(client):
    response = client.post('/api/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'role': 'user',
        'city': 'Mumbai',
        'budget_preference': 'mid',
        'preferred_sports': ['football', 'cricket'],
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'token' in data
    assert data['role'] == 'user'


def test_login(client):
    # Register first
    client.post('/api/register', json={
        'name': 'Login Test',
        'email': 'login@example.com',
        'password': 'pass123',
        'role': 'user',
    })
    # Then login
    response = client.post('/api/login', json={
        'email': 'login@example.com',
        'password': 'pass123',
    })
    assert response.status_code == 200
    assert 'token' in response.get_json()


def test_admin_cannot_register_publicly(client):
    response = client.post('/api/register', json={
        'name': 'Admin Attempt',
        'email': 'admin@test.com',
        'password': 'xyz',
        'role': 'admin',
    })
    assert response.status_code == 403
