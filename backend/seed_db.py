import os
import sys
from datetime import datetime, timedelta

# Add backend to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from app import create_app, db
from app.models.user import User
from app.models.event import Event
from app.models.registration import Registration
from app.models.payment import Payment

def seed_database():
    app = create_app()
    with app.app_context():
        print("Clearing database...")
        db.drop_all()
        db.create_all()

        print("Seeding Users...")
        admin = User(name='Admin Boss', email='admin@example.com', role='admin', city='Mumbai')
        admin.set_password('123456')
        
        org1 = User(name='Sports Authority', email='org1@example.com', role='organizer', city='Delhi')
        org1.set_password('123456')

        org2 = User(name='Active Life Org', email='org2@example.com', role='organizer', city='Bangalore')
        org2.set_password('123456')

        user1 = User(name='Rahul Sharma', email='user1@example.com', role='user', city='Delhi', budget_preference='mid', preferred_sports=['Football', 'Cricket'])
        user1.set_password('123456')

        user2 = User(name='Priya Patel', email='user2@example.com', role='user', city='Mumbai', budget_preference='cheap', preferred_sports=['Running', 'Cycling'])
        user2.set_password('123456')

        db.session.add_all([admin, org1, org2, user1, user2])
        db.session.commit()

        print("Seeding Events...")
        now = datetime.utcnow()
        e1 = Event(title='Delhi Monsoon Marathon', sport_category='Running', description='A 10k run through central Delhi.', venue_city='Delhi', venue_address='India Gate', event_date=now + timedelta(days=10), capacity=100, price=500, organizer_id=org1.id, is_active=True)
        e1.save()

        e2 = Event(title='Corporate Football League', sport_category='Football', description='5v5 tournament.', venue_city='Delhi', venue_address='Saket Sports Complex', event_date=now + timedelta(days=5), capacity=16, price=2500, organizer_id=org1.id, is_active=True)
        e2.save()

        e3 = Event(title='Mumbai Midnight Cycling', sport_category='Cycling', description='Night ride through South Bombay.', venue_city='Mumbai', venue_address='Colaba', event_date=now + timedelta(days=2), capacity=50, price=300, organizer_id=org2.id, is_active=True)
        e3.save()

        e4 = Event(title='Pro Tennis Workshop', sport_category='Tennis', description='Weekend coaching clinic.', venue_city='Bangalore', venue_address='KSLTA Stadium', event_date=now + timedelta(days=20), capacity=20, price=5000, organizer_id=org2.id, is_active=True)
        e4.save()

        print("Seeding Registrations & Payments...")
        # User 1 registers for E1
        r1 = Registration(user_id=user1.id, event_id=e1.id, status='confirmed')
        db.session.add(r1)
        db.session.commit()
        p1 = Payment(registration_id=r1.id, razorpay_order_id='order_mock1', razorpay_payment_id='pay_mock1', razorpay_signature='sig1', amount=e1.price, platform_fee=e1.price*0.15, organizer_payout=e1.price*0.85, status='paid')
        db.session.add(p1)

        # User 2 registers for E3
        r2 = Registration(user_id=user2.id, event_id=e3.id, status='confirmed')
        db.session.add(r2)
        db.session.commit()
        p2 = Payment(registration_id=r2.id, razorpay_order_id='order_mock2', razorpay_payment_id='pay_mock2', razorpay_signature='sig2', amount=e3.price, platform_fee=e3.price*0.15, organizer_payout=e3.price*0.85, status='paid')
        db.session.add(p2)

        # User 1 registers for E2
        r3 = Registration(user_id=user1.id, event_id=e2.id, status='confirmed')
        db.session.add(r3)
        db.session.commit()
        p3 = Payment(registration_id=r3.id, razorpay_order_id='order_mock3', razorpay_payment_id='pay_mock3', razorpay_signature='sig3', amount=e2.price, platform_fee=e2.price*0.15, organizer_payout=e2.price*0.85, status='paid')
        db.session.add(p3)

        db.session.commit()
        print("Database seeding complete!")

if __name__ == '__main__':
    seed_database()
