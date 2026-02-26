from app import create_app, db
from app.models import Event, User
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    # 1. Create a test user if it doesn't exist
    user = User.query.filter_by(email='user@test.io').first()
    if not user:
        user = User(
            name='Test User',
            email='user@test.io',
            password_hash=generate_password_hash('password123'),
            role='user',
            city='Mumbai',
            budget_preference='mid'
        )
        db.session.add(user)
    
    # 2. Clear old events and add new high-profile sports events
    Event.query.delete()
    
    events = [
        Event(
            title="Neon City Football Cup 2026",
            description="The ultimate urban football showdown.",
            sport_category="Football",
            venue_name="Cyber Arena",
            venue_city="Mumbai",
            event_date=datetime.now() + timedelta(days=14),
            price=1500.00,
            price_tier="mid",
            visibility="public"
        ),
        Event(
            title="Underground Cricket League",
            description="Street cricket goes pro. High stakes.",
            sport_category="Cricket",
            venue_name="Streets of Delhi",
            venue_city="Delhi",
            event_date=datetime.now() + timedelta(days=5),
            price=450.00,
            price_tier="cheap",
            visibility="public"
        ),
        Event(
            title="Vanguard Tennis Open",
            description="Premium court-side experiences.",
            sport_category="Tennis",
            venue_name="Sky Courts",
            venue_city="Bangalore",
            event_date=datetime.now() + timedelta(days=30),
            price=3000.00,
            price_tier="premium",
            visibility="public"
        )
    ]
    
    for e in events:
        db.session.add(e)
        
    db.session.commit()
    print("Database seeded with test user (user@test.io / password123) and new neon events.")

