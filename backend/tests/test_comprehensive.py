"""
Comprehensive tests for Sports Event Management API.
Covers all 3 roles: admin, organizer, user.
CRUD operations: Auth, Events, Registrations, Admin endpoints, Organizer endpoints.
"""
import pytest
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db as _db
from app.models.user import User
from app.models.event import Event
from app.models.registration import Registration


# ─────────────────────────── Fixtures ───────────────────────────

@pytest.fixture(scope='function')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # tokens don't expire in tests
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def seeded_db(app):
    """Seed admin, organizer, and user accounts + events into the in-memory DB."""
    with app.app_context():
        admin = User(name='Admin Boss', email='admin@example.com', role='admin', city='Mumbai')
        admin.set_password('123456')

        org = User(name='Sports Authority', email='org1@example.com', role='organizer', city='Delhi')
        org.set_password('123456')

        user = User(name='Rahul Sharma', email='user1@example.com', role='user',
                    city='Delhi', budget_preference='mid',
                    preferred_sports=['Football', 'Cricket'])
        user.set_password('123456')

        _db.session.add_all([admin, org, user])
        _db.session.commit()

        # Create an event owned by 'org'
        event = Event(
            title='Test Marathon',
            sport_category='Running',
            description='A test 10k run.',
            venue_city='Delhi',
            venue_address='India Gate',
            event_date=datetime.utcnow() + timedelta(days=10),
            capacity=100,
            price=500.0,
            organizer_id=org.id,
            is_active=True
        )
        event.save()

        yield {
            'admin_id': admin.id,
            'org_id': org.id,
            'user_id': user.id,
            'event_id': event.id
        }


def login(client, email, password='123456'):
    """Helper: login and return the Bearer token string."""
    r = client.post('/api/auth/login', json={'email': email, 'password': password})
    assert r.status_code == 200, f"Login failed for {email}: {r.get_json()}"
    return r.get_json()['access_token']


def auth_headers(token):
    return {'Authorization': f'Bearer {token}'}


# ─────────────────────────── AUTH ───────────────────────────────

class TestAuth:
    def test_register_user(self, client):
        r = client.post('/api/auth/register', json={
            'name': 'New User',
            'email': 'newuser@test.com',
            'password': 'pass1234',
            'role': 'user',
            'city': 'Mumbai',
        })
        assert r.status_code == 201
        data = r.get_json()
        assert 'access_token' in data
        assert 'user_id' in data

    def test_register_organizer(self, client):
        r = client.post('/api/auth/register', json={
            'name': 'Org User',
            'email': 'org@test.com',
            'password': 'pass1234',
            'role': 'organizer',
        })
        assert r.status_code == 201
        assert 'access_token' in r.get_json()

    def test_register_admin_blocked(self, client):
        r = client.post('/api/auth/register', json={
            'name': 'Admin', 'email': 'a@t.com', 'password': 'x', 'role': 'admin'
        })
        assert r.status_code == 403

    def test_register_duplicate_email(self, client):
        payload = {'name': 'A', 'email': 'dup@t.com', 'password': 'p', 'role': 'user'}
        client.post('/api/auth/register', json=payload)
        r = client.post('/api/auth/register', json=payload)
        assert r.status_code == 400

    def test_login_valid(self, client, seeded_db):
        r = client.post('/api/auth/login', json={'email': 'user1@example.com', 'password': '123456'})
        assert r.status_code == 200
        data = r.get_json()
        assert 'access_token' in data
        assert data['role'] == 'user'

    def test_login_wrong_password(self, client, seeded_db):
        r = client.post('/api/auth/login', json={'email': 'user1@example.com', 'password': 'wrong'})
        assert r.status_code == 401

    def test_login_unknown_email(self, client):
        r = client.post('/api/auth/login', json={'email': 'nobody@x.com', 'password': '123456'})
        assert r.status_code == 401

    def test_get_profile(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        r = client.get('/api/auth/me', headers=auth_headers(token))
        assert r.status_code == 200
        data = r.get_json()
        assert data['email'] == 'user1@example.com'
        assert data['role'] == 'user'

    def test_update_profile(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        r = client.put('/api/auth/me', json={'city': 'Bangalore', 'budget_preference': 'premium'},
                       headers=auth_headers(token))
        assert r.status_code == 200
        data = r.get_json()
        assert data['city'] == 'Bangalore'
        assert data['budget_preference'] == 'premium'

    def test_profile_requires_auth(self, client):
        r = client.get('/api/auth/me')
        assert r.status_code == 401


# ─────────────────────────── EVENTS ─────────────────────────────

class TestEvents:
    def test_list_events_public(self, client, seeded_db):
        r = client.get('/api/events')
        assert r.status_code == 200
        assert isinstance(r.get_json(), list)

    def test_get_single_event(self, client, seeded_db):
        event_id = seeded_db['event_id']
        r = client.get(f'/api/events/{event_id}')
        assert r.status_code == 200
        data = r.get_json()
        assert data['id'] == event_id
        assert data['title'] == 'Test Marathon'

    def test_get_nonexistent_event(self, client, seeded_db):
        r = client.get('/api/events/99999')
        assert r.status_code == 404

    def test_organizer_can_create_event(self, client, seeded_db):
        token = login(client, 'org1@example.com')
        r = client.post('/api/events', json={
            'title': 'New Football Tourney',
            'sport_category': 'Football',
            'description': '5v5 tournament',
            'venue_city': 'Mumbai',
            'venue_address': 'BKC Ground',
            'event_date': (datetime.utcnow() + timedelta(days=15)).isoformat(),
            'capacity': 32,
            'price': 1500.0,
        }, headers=auth_headers(token))
        assert r.status_code == 201
        data = r.get_json()
        assert data['title'] == 'New Football Tourney'
        assert data['price_tier'] == 'mid'

    def test_user_cannot_create_event(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        r = client.post('/api/events', json={
            'title': 'Unauthorized Event',
            'sport_category': 'Cricket',
            'event_date': (datetime.utcnow() + timedelta(days=5)).isoformat(),
            'capacity': 10, 'price': 100.0,
        }, headers=auth_headers(token))
        assert r.status_code == 403

    def test_create_event_requires_auth(self, client, seeded_db):
        r = client.post('/api/events', json={'title': 'No Auth', 'sport_category': 'Cricket',
                                              'event_date': datetime.utcnow().isoformat(),
                                              'capacity': 10, 'price': 100.0})
        assert r.status_code == 401

    def test_organizer_can_update_own_event(self, client, seeded_db):
        token = login(client, 'org1@example.com')
        event_id = seeded_db['event_id']
        r = client.put(f'/api/events/{event_id}',
                       json={'title': 'Updated Marathon', 'capacity': 200},
                       headers=auth_headers(token))
        assert r.status_code == 200
        assert r.get_json()['title'] == 'Updated Marathon'

    def test_other_organizer_cannot_update_event(self, client, seeded_db):
        # Register a second organizer
        client.post('/api/auth/register', json={
            'name': 'Second Org', 'email': 'org2@test.com', 'password': 'pass', 'role': 'organizer'
        })
        token2 = login(client, 'org2@test.com', 'pass')
        event_id = seeded_db['event_id']
        r = client.put(f'/api/events/{event_id}',
                       json={'title': 'Hijacked Event'},
                       headers=auth_headers(token2))
        assert r.status_code == 403

    def test_organizer_can_delete_own_event(self, client, seeded_db):
        token = login(client, 'org1@example.com')
        event_id = seeded_db['event_id']
        r = client.delete(f'/api/events/{event_id}', headers=auth_headers(token))
        assert r.status_code == 200
        # Verify it's now inactive (soft delete)
        r2 = client.get(f'/api/events/{event_id}')
        assert r2.status_code == 404

    def test_admin_can_delete_any_event(self, client, seeded_db):
        token = login(client, 'admin@example.com')
        event_id = seeded_db['event_id']
        r = client.delete(f'/api/events/{event_id}', headers=auth_headers(token))
        assert r.status_code == 200

    def test_user_cannot_delete_event(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        event_id = seeded_db['event_id']
        r = client.delete(f'/api/events/{event_id}', headers=auth_headers(token))
        assert r.status_code == 403

    def test_similar_events(self, client, seeded_db):
        event_id = seeded_db['event_id']
        r = client.get(f'/api/events/{event_id}/similar')
        assert r.status_code == 200
        assert isinstance(r.get_json(), list)


# ─────────────────────────── REGISTRATIONS ──────────────────────

class TestRegistrations:
    def test_user_can_register_for_event(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        event_id = seeded_db['event_id']
        r = client.post('/api/registrations', json={'event_id': event_id},
                        headers=auth_headers(token))
        assert r.status_code == 201
        data = r.get_json()
        assert 'registration_id' in data

    def test_duplicate_registration_blocked(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        event_id = seeded_db['event_id']
        # First registration
        client.post('/api/registrations', json={'event_id': event_id}, headers=auth_headers(token))
        # Second registration for same event
        r = client.post('/api/registrations', json={'event_id': event_id}, headers=auth_headers(token))
        assert r.status_code == 400

    def test_register_nonexistent_event(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        r = client.post('/api/registrations', json={'event_id': 99999},
                        headers=auth_headers(token))
        assert r.status_code == 404

    def test_organizer_cannot_register_for_event(self, client, seeded_db):
        token = login(client, 'org1@example.com')
        event_id = seeded_db['event_id']
        r = client.post('/api/registrations', json={'event_id': event_id},
                        headers=auth_headers(token))
        assert r.status_code == 403

    def test_user_can_view_own_registrations(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        event_id = seeded_db['event_id']
        client.post('/api/registrations', json={'event_id': event_id}, headers=auth_headers(token))
        r = client.get('/api/registrations/my', headers=auth_headers(token))
        assert r.status_code == 200
        regs = r.get_json()
        assert len(regs) >= 1
        assert regs[0]['event_id'] == event_id

    def test_user_can_cancel_registration(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        event_id = seeded_db['event_id']
        # Register
        reg_r = client.post('/api/registrations', json={'event_id': event_id},
                            headers=auth_headers(token))
        reg_id = reg_r.get_json()['registration_id']
        # Cancel
        r = client.put(f'/api/registrations/{reg_id}/cancel', headers=auth_headers(token))
        assert r.status_code == 200
        assert r.get_json()['registration']['status'] == 'cancelled'

    def test_cancel_nonexistent_registration(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        r = client.put('/api/registrations/99999/cancel', headers=auth_headers(token))
        assert r.status_code == 404

    def test_cannot_cancel_already_cancelled(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        event_id = seeded_db['event_id']
        reg_r = client.post('/api/registrations', json={'event_id': event_id},
                            headers=auth_headers(token))
        reg_id = reg_r.get_json()['registration_id']
        client.put(f'/api/registrations/{reg_id}/cancel', headers=auth_headers(token))
        # Cancel again
        r = client.put(f'/api/registrations/{reg_id}/cancel', headers=auth_headers(token))
        assert r.status_code == 400


# ─────────────────────────── ADMIN ──────────────────────────────

class TestAdmin:
    def test_admin_dashboard(self, client, seeded_db):
        token = login(client, 'admin@example.com')
        r = client.get('/api/admin/dashboard', headers=auth_headers(token))
        assert r.status_code == 200
        data = r.get_json()
        assert 'total_users' in data
        assert 'total_events' in data
        assert 'total_registrations' in data
        assert 'total_revenue' in data

    def test_popular_sport(self, client, seeded_db):
        token = login(client, 'admin@example.com')
        r = client.get('/api/admin/popular-sport', headers=auth_headers(token))
        assert r.status_code == 200
        assert isinstance(r.get_json(), list)

    def test_city_distribution(self, client, seeded_db):
        token = login(client, 'admin@example.com')
        r = client.get('/api/admin/city-distribution', headers=auth_headers(token))
        assert r.status_code == 200
        assert isinstance(r.get_json(), list)

    def test_fill_rate(self, client, seeded_db):
        token = login(client, 'admin@example.com')
        r = client.get('/api/admin/fill-rate', headers=auth_headers(token))
        assert r.status_code == 200
        assert isinstance(r.get_json(), list)

    def test_monthly_trend(self, client, seeded_db):
        token = login(client, 'admin@example.com')
        r = client.get('/api/admin/monthly-trend', headers=auth_headers(token))
        assert r.status_code == 200
        assert isinstance(r.get_json(), list)

    def test_organizer_performance(self, client, seeded_db):
        token = login(client, 'admin@example.com')
        r = client.get('/api/admin/organizer-performance', headers=auth_headers(token))
        assert r.status_code == 200
        assert isinstance(r.get_json(), list)

    def test_escalations_list(self, client, seeded_db):
        token = login(client, 'admin@example.com')
        r = client.get('/api/admin/escalations', headers=auth_headers(token))
        assert r.status_code == 200
        assert isinstance(r.get_json(), list)

    # Role guard: user cannot access admin endpoints
    def test_user_denied_admin_dashboard(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        r = client.get('/api/admin/dashboard', headers=auth_headers(token))
        assert r.status_code == 403

    # Role guard: organizer cannot access admin endpoints
    def test_organizer_denied_admin_dashboard(self, client, seeded_db):
        token = login(client, 'org1@example.com')
        r = client.get('/api/admin/dashboard', headers=auth_headers(token))
        assert r.status_code == 403

    def test_unauthenticated_denied_admin(self, client):
        r = client.get('/api/admin/dashboard')
        assert r.status_code == 401


# ─────────────────────────── ORGANIZER ──────────────────────────

class TestOrganizer:
    def test_organizer_dashboard(self, client, seeded_db):
        token = login(client, 'org1@example.com')
        r = client.get('/api/organizer/dashboard', headers=auth_headers(token))
        assert r.status_code == 200
        data = r.get_json()
        assert isinstance(data, list)
        # The seeded organizer has 1 event
        assert len(data) >= 1
        assert 'title' in data[0]
        assert 'fill_rate' in data[0]

    def test_ticket_summary(self, client, seeded_db):
        token = login(client, 'org1@example.com')
        r = client.get('/api/organizer/ticket-summary', headers=auth_headers(token))
        assert r.status_code == 200
        assert isinstance(r.get_json(), list)

    def test_category_insight(self, client, seeded_db):
        token = login(client, 'org1@example.com')
        r = client.get('/api/organizer/category-insight', headers=auth_headers(token))
        assert r.status_code == 200
        assert isinstance(r.get_json(), list)

    def test_registration_trend(self, client, seeded_db):
        token = login(client, 'org1@example.com')
        event_id = seeded_db['event_id']
        r = client.get(f'/api/organizer/trend/{event_id}', headers=auth_headers(token))
        assert r.status_code == 200
        assert isinstance(r.get_json(), list)

    def test_user_denied_organizer_dashboard(self, client, seeded_db):
        token = login(client, 'user1@example.com')
        r = client.get('/api/organizer/dashboard', headers=auth_headers(token))
        assert r.status_code == 403

    def test_unauthenticated_denied_organizer(self, client):
        r = client.get('/api/organizer/dashboard')
        assert r.status_code == 401

    def test_feature_event_toggle(self, client, seeded_db):
        token = login(client, 'org1@example.com')
        event_id = seeded_db['event_id']
        r = client.post(f'/api/organizer/events/{event_id}/feature',
                        headers=auth_headers(token))
        assert r.status_code == 200
        data = r.get_json()
        assert 'is_featured' in data
        assert data['is_featured'] is True  # was False, now toggled to True
