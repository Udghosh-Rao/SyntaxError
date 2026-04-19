"""
seed_db.py — Rich realistic seed data for the LiveSports platform.

What's seeded:
  ┌─────────────────────────────────────────────────────────────────┐
  │  1 admin                                                        │
  │  5 organizers (diverse cities & sport categories)               │
  │  25 events  (past / near-future / far-future; free & paid)      │
  │  22 regular users (varied cities, budgets, preferred sports)     │
  │  ~70 registrations + payments                                   │
  │                                                                 │
  │  Edge cases:                                                    │
  │    • 2 cold-start users with no bookings                        │
  │    • 1 pending (unpaid) registration                            │
  │    • 1 cancelled registration                                   │
  │    • 2 highly-active / power users                              │
  │    • Overlapping interests → collaborative filtering signal      │
  └─────────────────────────────────────────────────────────────────┘

Recommendation engine alignment (from RecommendationService):
  sport_category match  → +40 pts
  city match            → +30 pts
  price_tier match      → +20 pts
  event within 7 days   → +10 pts
  is_featured           → always surfaces first
"""

import os
import sys
import random
from datetime import datetime, timedelta

# ── Reproducibility ──────────────────────────────────────────────────────────
random.seed(42)

# Make sure the backend package is importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.extensions import db
from app.models.user import User, generate_referral_code
from app.models.event import Event
from app.models.registration import Registration
from app.models.payment import Payment


# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def make_user(name: str, email: str, role: str, city: str,
              budget: str, sports: list) -> User:
    """
    Construct a User instance.
    budget must be one of: 'cheap' | 'mid' | 'premium'
    sports is a list of sport category strings matching Event.sport_category values.
    """
    # Ensure unique referral code
    code = generate_referral_code()
    while User.query.filter_by(referral_code=code).first():
        code = generate_referral_code()

    u = User(
        name=name,
        email=email,
        role=role,
        city=city,
        budget_preference=budget,
        preferred_sports=sports,
        referral_code=code,
    )
    u.set_password('123456')
    return u


def make_event(organizer_id: int, title: str, sport_category: str,
               description: str, venue_city: str, venue_address: str,
               days_from_now: int, capacity: int, price: float,
               tags: list, is_featured: bool = False,
               banner_url: str = None) -> Event:
    """
    Construct an Event instance.
    Call .save() after adding to session to auto-compute price_tier.
    days_from_now < 0  → past event
    days_from_now 0-7  → near-future (recommendation bonus)
    days_from_now > 7  → far-future
    price_tier auto-computed by Event.save():
        < 500   → 'cheap'
        <= 2000 → 'mid'
        > 2000  → 'premium'
    """
    return Event(
        organizer_id=organizer_id,
        title=title,
        sport_category=sport_category,
        description=description,
        venue_city=venue_city,
        venue_address=venue_address,
        event_date=datetime.utcnow() + timedelta(days=days_from_now),
        capacity=capacity,
        price=float(price),
        tags=tags,
        banner_url=banner_url,
        is_active=True,
        is_featured=is_featured,
    )


def create_registration(user_id: int, event_id: int,
                        status: str = 'confirmed',
                        created_at: datetime | None = None) -> Registration:
    """Construct a Registration instance."""
    reg = Registration(
        user_id=user_id,
        event_id=event_id,
        status=status,
        role='athlete',
        role_details={},
    )
    if created_at:
        reg.created_at = created_at
    return reg


def create_payment(registration_id: int, amount: float,
                   paid: bool = True,
                   created_at: datetime | None = None) -> Payment:
    """
    Construct a Payment instance.
    paid=True  → status='paid'   (normal confirmed booking)
    paid=False → status='created' (order placed, user hasn't completed checkout)
    Platform fee: 15 % (mirrors PLATFORM_FEE default in config).
    """
    fee = round(amount * 0.15, 2)
    payout = round(amount - fee, 2)
    payment = Payment(
        registration_id=registration_id,
        razorpay_order_id=f'order_seed_{registration_id}',
        razorpay_payment_id=f'pay_seed_{registration_id}' if paid else None,
        razorpay_signature=f'sig_seed_{registration_id}' if paid else None,
        amount=amount,
        platform_fee=fee,
        organizer_payout=payout,
        status='paid' if paid else 'created',
    )
    if created_at:
        payment.created_at = created_at
    return payment


def safe_register(user: User, event: Event,
                  status: str = 'confirmed',
                  created_at: datetime | None = None) -> Registration | None:
    """
    Register a user for an event with guards:
      • Skip if event is at capacity
      • Skip if duplicate registration exists (UniqueConstraint guard)
    Free events (price == 0) get confirmed status with no payment.
    Paid events get a payment record.
    Returns the Registration object, or None if skipped.
    """
    # Capacity guard
    if event.seats_remaining <= 0:
        print(f'    [SKIP] {user.name} -> {event.title}: sold out')
        return None

    # Duplicate guard
    existing = Registration.query.filter_by(
        user_id=user.id, event_id=event.id
    ).first()
    if existing:
        return None

    reg = create_registration(user.id, event.id, status=status, created_at=created_at)
    db.session.add(reg)
    db.session.commit()   # commit so reg.id is available for payment FK

    # Payment record for paid events with confirmed status
    if event.price > 0 and status == 'confirmed':
        payment_created_at = None
        if created_at:
            payment_created_at = created_at + timedelta(minutes=random.randint(1, 180))
        payment = create_payment(reg.id, event.price, paid=True, created_at=payment_created_at)
        db.session.add(payment)
        db.session.commit()

    return reg


# ═══════════════════════════════════════════════════════════════════
# MAIN SEED FUNCTION
# ═══════════════════════════════════════════════════════════════════

def seed_database():
    app = create_app()
    with app.app_context():

        # ── 0. Wipe & recreate all tables ─────────────────────────────────
        print('Clearing database ...')
        db.drop_all()
        db.create_all()

        # ─────────────────────────────────────────────────────────────────
        # 1. ADMIN
        # ─────────────────────────────────────────────────────────────────
        print('\nSeeding admin ...')
        admin = make_user('Admin Boss', 'admin@livesports.in',
                          'admin', 'Mumbai', 'premium', [])
        db.session.add(admin)
        db.session.commit()

        # ─────────────────────────────────────────────────────────────────
        # 2. ORGANIZERS  (5 organizers across different cities & sports)
        # ─────────────────────────────────────────────────────────────────
        print('\nSeeding organizers ...')

        organizers_raw = [
            # (name, email, city, budget, preferred_sports)
            (
                'Sports Authority India',
                'org1@gmail.com',
                'Delhi', 'premium',
                ['Football', 'Athletics', 'Cricket'],
            ),
            (
                'ActiveLife Events',
                'org2@gmail.com',
                'Bangalore', 'mid',
                ['Running', 'Cycling', 'Yoga'],
            ),
            (
                'Premier Cricket Club',
                'org3@gmail.com',
                'Mumbai', 'premium',
                ['Cricket', 'Football'],
            ),
            (
                'TechFit Sports',
                'org4@gmail.com',
                'Pune', 'mid',
                ['Basketball', 'Badminton', 'Running'],
            ),
            (
                'South Sports Academy',
                'org5@gmail.com',
                'Chennai', 'cheap',
                ['Tennis', 'Swimming', 'Athletics'],
            ),
        ]

        organizers: list[User] = []
        for name, email, city, budget, sports in organizers_raw:
            o = make_user(name, email, 'organizer', city, budget, sports)
            db.session.add(o)
            organizers.append(o)
        db.session.commit()
        print(f'  -> {len(organizers)} organizers created')

        # ─────────────────────────────────────────────────────────────────
        # 3. EVENTS  (5 per organizer = 25 total)
        #
        # Index map for quick reference when building booking_map:
        #
        #  SPORTS AUTHORITY INDIA (org 0, Delhi)
        #   [0]  Delhi Premier Football League     Football   ₹2500 premium  future+5
        #   [1]  National Athletics Championship   Athletics  ₹1500 mid      past −10
        #   [2]  Delhi Half Marathon 2025          Running    ₹799  mid      future+30
        #   [3]  Cricket Carnival – T10 Blitz      Cricket    ₹3000 premium  past −5
        #   [4]  Free Fitness Boot Camp            Athletics  FREE           future+3
        #
        #  ACTIVELIFE EVENTS (org 1, Bangalore)
        #   [5]  Bangalore Night Cycling Ride      Cycling    ₹399  cheap    future+2
        #   [6]  Sunrise Yoga at Lalbagh           Yoga       FREE           future+1
        #   [7]  Bangalore 10K – Women's Special   Running    ₹499  cheap    future+15
        #   [8]  Trail Cycling – Coorg Edition     Cycling    ₹4500 premium  future+45
        #   [9]  Zen Yoga & Meditation Retreat     Yoga       ₹2999 premium  past −20
        #
        #  PREMIER CRICKET CLUB (org 2, Mumbai)
        #  [10]  Mumbai T20 Street Cricket Fest    Cricket    ₹1999 mid      future+6
        #  [11]  IPL Watch Party & Nets Session    Cricket    ₹999  mid      future+4
        #  [12]  Kids Cricket Academy – Summer     Cricket    ₹5000 premium  future+20
        #  [13]  Corporate Cricket Challenge       Cricket    ₹2500 premium  past −15
        #  [14]  Beach Football & Cricket Combo    Football   ₹599  mid      future+7
        #
        #  TECHFIT SPORTS (org 3, Pune)
        #  [15]  Pune Basketball League–Season 3   Basketball ₹1500 mid      future+10
        #  [16]  Badminton Super Series – Pune     Badminton  ₹800  mid      past −8
        #  [17]  Monsoon Run – Pune Mud Race       Running    ₹1200 mid      future+25
        #  [18]  Beginner Basketball Clinic        Basketball FREE           future+12
        #  [19]  Badminton & Breakfast Mixer       Badminton  ₹349  cheap    future+3
        #
        #  SOUTH SPORTS ACADEMY (org 4, Chennai)
        #  [20]  Chennai Open Tennis Tournament    Tennis     ₹2000 mid      future+18
        #  [21]  Summer Swim Gala – All Levels     Swimming   ₹750  mid      future+8
        #  [22]  Kids Tennis Coaching Weekend      Tennis     ₹1500 mid      past −3
        #  [23]  Open Water Swimming Challenge     Swimming   ₹1800 mid      future+35
        #  [24]  Free Athlete Fitness Assessment   Athletics  FREE           future+1
        # ─────────────────────────────────────────────────────────────────
        print('\nSeeding events ...')

        events_raw = [
            # ── Sports Authority India (org idx 0) ──────────────────────────
            dict(
                org=0, title='Delhi Premier Football League',
                sport_category='Football',
                description=(
                    'A high-octane 5v5 football tournament across 8 teams. '
                    'Winners receive ₹50,000 in prize money.'
                ),
                venue_city='Delhi', venue_address='Jawaharlal Nehru Stadium',
                days=5, capacity=32, price=2500.0,
                tags=['football', 'tournament', 'competitive', 'corporate'],
                is_featured=True,
                banner_url='https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800',
            ),
            dict(
                org=0, title='National Athletics Championship',
                sport_category='Athletics',
                description=(
                    '100 m, 200 m, long jump and hurdles open to all age groups. '
                    'Certified timing system in use.'
                ),
                venue_city='Delhi', venue_address='Indira Gandhi Indoor Stadium',
                days=-10, capacity=200, price=1500.0,
                tags=['athletics', 'track', 'championship', 'sprint'],
                is_featured=False,
            ),
            dict(
                org=0, title='Delhi Half Marathon 2025',
                sport_category='Running',
                description=(
                    'Run 21 km through iconic Delhi landmarks — India Gate, '
                    'Rajpath and Lodhi Garden. All finishers get a medal.'
                ),
                venue_city='Delhi', venue_address='India Gate',
                days=30, capacity=500, price=799.0,
                tags=['running', 'half-marathon', 'fitness', 'outdoors'],
                is_featured=True,
                banner_url='https://images.unsplash.com/photo-1529347666754-5db7740c1748?w=800',
            ),
            dict(
                org=0, title='Cricket Carnival – T10 Blitz',
                sport_category='Cricket',
                description=(
                    'Fast-paced T10 format cricket. 6 teams, double elimination. '
                    'The quickest form of cricket comes to Delhi.'
                ),
                venue_city='Delhi', venue_address='Kotla Cricket Ground',
                days=-5, capacity=24, price=3000.0,
                tags=['cricket', 't10', 'tournament', 'fast-format'],
                is_featured=False,
            ),
            dict(
                org=0, title='Free Fitness Boot Camp',
                sport_category='Athletics',
                description=(
                    'High-intensity interval training session open to all fitness '
                    'levels. Bring water, wear comfortable shoes.'
                ),
                venue_city='Delhi', venue_address='Lodhi Garden',
                days=3, capacity=100, price=0.0,
                tags=['fitness', 'bootcamp', 'free', 'outdoor', 'hiit'],
                is_featured=False,
            ),

            # ── ActiveLife Events (org idx 1) ────────────────────────────────
            dict(
                org=1, title='Bangalore Night Cycling Ride',
                sport_category='Cycling',
                description=(
                    'A scenic 40 km night ride through the foothills of Nandi Hills. '
                    'Safety lights provided. Breakfast included.'
                ),
                venue_city='Bangalore', venue_address='Cubbon Park Gate',
                days=2, capacity=80, price=399.0,
                tags=['cycling', 'night-ride', 'outdoor', 'group'],
                is_featured=True,
                banner_url='https://images.unsplash.com/photo-1558981852-426c349d0039?w=800',
            ),
            dict(
                org=1, title='Sunrise Yoga at Lalbagh',
                sport_category='Yoga',
                description=(
                    'Start your day with peace and flexibility in Bangalore\'s '
                    'beautiful Lalbagh Botanical Garden. All levels welcome.'
                ),
                venue_city='Bangalore', venue_address='Lalbagh Botanical Garden',
                days=1, capacity=60, price=0.0,
                tags=['yoga', 'wellness', 'free', 'morning', 'mindfulness'],
                is_featured=False,
            ),
            dict(
                org=1, title='Bangalore 10K – Women\'s Special',
                sport_category='Running',
                description=(
                    'An all-women\'s 10K celebrating fitness, community and '
                    'empowerment. Timed event with medals for all finishers.'
                ),
                venue_city='Bangalore', venue_address='MG Road Start Point',
                days=15, capacity=300, price=499.0,
                tags=['running', 'womens', 'community', '10k', 'timed'],
                is_featured=False,
            ),
            dict(
                org=1, title='Trail Cycling – Coorg Edition',
                sport_category='Cycling',
                description=(
                    'A two-day trail cycling adventure through Coorg\'s coffee '
                    'forests. Accommodation, meals, and guide included.'
                ),
                venue_city='Bangalore', venue_address='Coorg Base Camp',
                days=45, capacity=30, price=4500.0,
                tags=['cycling', 'trail', 'adventure', 'premium', 'overnight'],
                is_featured=True,
                banner_url='https://images.unsplash.com/photo-1571188654248-7a89213915f7?w=800',
            ),
            dict(
                org=1, title='Zen Yoga & Meditation Retreat',
                sport_category='Yoga',
                description=(
                    'A weekend wellness retreat combining yoga asanas, breathwork '
                    'and guided meditation. Vegetarian meals included.'
                ),
                venue_city='Bangalore', venue_address='Jayanagar Community Hall',
                days=-20, capacity=40, price=2999.0,
                tags=['yoga', 'meditation', 'retreat', 'wellness', 'weekend'],
                is_featured=False,
            ),

            # ── Premier Cricket Club (org idx 2) ────────────────────────────
            dict(
                org=2, title='Mumbai T20 Street Cricket Fest',
                sport_category='Cricket',
                description=(
                    'Street cricket carnival with teams from 8 zones of Mumbai. '
                    'Live commentary, DJ, and food stalls.'
                ),
                venue_city='Mumbai', venue_address='Shivaji Park',
                days=6, capacity=128, price=1999.0,
                tags=['cricket', 't20', 'street-cricket', 'festival', 'community'],
                is_featured=True,
                banner_url='https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=800',
            ),
            dict(
                org=2, title='IPL Watch Party & Nets Session',
                sport_category='Cricket',
                description=(
                    'Watch live IPL on a giant screen with fellow fans then '
                    'step into professional practice nets for a hands-on session.'
                ),
                venue_city='Mumbai', venue_address='Wankhede Stadium Nets',
                days=4, capacity=50, price=999.0,
                tags=['cricket', 'ipl', 'watch-party', 'nets', 'coaching'],
                is_featured=False,
            ),
            dict(
                org=2, title='Kids Cricket Academy – Summer Camp',
                sport_category='Cricket',
                description=(
                    '3-week intensive coaching camp for children aged 8–15. '
                    'Covers batting, bowling, fielding and match strategy.'
                ),
                venue_city='Mumbai', venue_address='Cross Maidan',
                days=20, capacity=40, price=5000.0,
                tags=['cricket', 'kids', 'coaching', 'summer-camp', 'training'],
                is_featured=False,
            ),
            dict(
                org=2, title='Corporate Cricket Challenge',
                sport_category='Cricket',
                description=(
                    'Inter-company cricket league played in the heart of Mumbai. '
                    'Build team spirit while competing against 8 corporate giants.'
                ),
                venue_city='Mumbai', venue_address='DY Patil Stadium',
                days=-15, capacity=64, price=2500.0,
                tags=['cricket', 'corporate', 'league', 'networking', 'team'],
                is_featured=False,
            ),
            dict(
                org=2, title='Beach Football & Cricket Combo',
                sport_category='Football',
                description=(
                    'Morning 5-a-side football on Juhu Beach followed by casual '
                    'beach cricket. Snacks and refreshments included.'
                ),
                venue_city='Mumbai', venue_address='Juhu Beach',
                days=7, capacity=40, price=599.0,
                tags=['football', 'cricket', 'beach', 'outdoor', 'casual'],
                is_featured=False,
            ),

            # ── TechFit Sports (org idx 3) ───────────────────────────────────
            dict(
                org=3, title='Pune Basketball League – Season 3',
                sport_category='Basketball',
                description=(
                    'City-wide 3×3 basketball tournament across 6 outdoor courts. '
                    'Prize pool of ₹20,000 for the winning team.'
                ),
                venue_city='Pune', venue_address='Shree Shiv Chhatrapati Sports Complex',
                days=10, capacity=48, price=1500.0,
                tags=['basketball', 'league', '3x3', 'competitive', 'outdoor'],
                is_featured=True,
                banner_url='https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800',
            ),
            dict(
                org=3, title='Badminton Super Series – Pune',
                sport_category='Badminton',
                description=(
                    'Open badminton tournament covering all categories: '
                    'singles, doubles and mixed. BANS-certified referees.'
                ),
                venue_city='Pune', venue_address='Balewadi Indoor Stadium',
                days=-8, capacity=64, price=800.0,
                tags=['badminton', 'tournament', 'racket-sports', 'open'],
                is_featured=False,
            ),
            dict(
                org=3, title='Monsoon Run – Pune Mud Race',
                sport_category='Running',
                description=(
                    'A thrilling 5 km obstacle mud run for adventure seekers. '
                    'Navigate 12 obstacles across a wet terrain course.'
                ),
                venue_city='Pune', venue_address='Lavasa Outskirts',
                days=25, capacity=200, price=1200.0,
                tags=['running', 'mud-race', 'obstacle', 'adventure', 'fun'],
                is_featured=False,
                banner_url='https://images.unsplash.com/photo-1469395446868-fb6a048d5ca3?w=800',
            ),
            dict(
                org=3, title='Beginner Basketball Clinic',
                sport_category='Basketball',
                description=(
                    'Learn basketball fundamentals from NBA-certified coaches. '
                    'Perfect for complete beginners aged 12 and above.'
                ),
                venue_city='Pune', venue_address='Koregaon Park Courts',
                days=12, capacity=30, price=0.0,
                tags=['basketball', 'coaching', 'free', 'beginners', 'training'],
                is_featured=False,
            ),
            dict(
                org=3, title='Badminton & Breakfast Mixer',
                sport_category='Badminton',
                description=(
                    'Casual doubles badminton followed by a healthy breakfast '
                    'networking session. Great for professionals and hobbyists.'
                ),
                venue_city='Pune', venue_address='Aundh Sports Club',
                days=3, capacity=24, price=349.0,
                tags=['badminton', 'networking', 'casual', 'morning', 'social'],
                is_featured=False,
            ),

            # ── South Sports Academy (org idx 4) ────────────────────────────
            dict(
                org=4, title='Chennai Open Tennis Tournament',
                sport_category='Tennis',
                description=(
                    'Annual open tennis tournament with singles and doubles draws. '
                    'AITA ranking points available for eligible players.'
                ),
                venue_city='Chennai', venue_address='SDAT Tennis Stadium',
                days=18, capacity=64, price=2000.0,
                tags=['tennis', 'tournament', 'open', 'competitive', 'aita'],
                is_featured=True,
                banner_url='https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=800',
            ),
            dict(
                org=4, title='Summer Swim Gala – All Levels',
                sport_category='Swimming',
                description=(
                    'Competitive swim meet across 50 m, 100 m and 200 m freestyle '
                    'and backstroke events. All age groups welcome.'
                ),
                venue_city='Chennai', venue_address='Nehru Indoor Stadium Pool',
                days=8, capacity=80, price=750.0,
                tags=['swimming', 'gala', 'competition', 'aquatics', 'indoor'],
                is_featured=False,
            ),
            dict(
                org=4, title='Kids Tennis Coaching Weekend',
                sport_category='Tennis',
                description=(
                    'Two-day intensive on-court coaching for children aged 6–14. '
                    'Covers grip, footwork, groundstrokes and match play.'
                ),
                venue_city='Chennai', venue_address='SDAT Coaching Centre',
                days=-3, capacity=30, price=1500.0,
                tags=['tennis', 'kids', 'coaching', 'weekend', 'beginners'],
                is_featured=False,
            ),
            dict(
                org=4, title='Open Water Swimming Challenge',
                sport_category='Swimming',
                description=(
                    'A 2 km open-water swim in the Bay of Bengal under full '
                    'safety supervision. Kayak escorts and timing chips provided.'
                ),
                venue_city='Chennai', venue_address='Marina Beach Water Sports',
                days=35, capacity=50, price=1800.0,
                tags=['swimming', 'open-water', 'challenge', 'adventure', 'sea'],
                is_featured=False,
            ),
            dict(
                org=4, title='Free Athlete Fitness Assessment',
                sport_category='Athletics',
                description=(
                    'Free VO2 max, agility, flexibility and strength assessment '
                    'for all athletes. Get a personalised training report.'
                ),
                venue_city='Chennai', venue_address='SAI Training Centre Chennai',
                days=1, capacity=120, price=0.0,
                tags=['athletics', 'fitness', 'assessment', 'free', 'testing'],
                is_featured=False,
            ),
        ]

        events: list[Event] = []
        for raw in events_raw:
            e = make_event(
                organizer_id=organizers[raw['org']].id,
                title=raw['title'],
                sport_category=raw['sport_category'],
                description=raw['description'],
                venue_city=raw['venue_city'],
                venue_address=raw['venue_address'],
                days_from_now=raw['days'],
                capacity=raw['capacity'],
                price=raw['price'],
                tags=raw['tags'],
                is_featured=raw.get('is_featured', False),
                banner_url=raw.get('banner_url'),
            )
            e.save()   # auto-computes price_tier and commits
            events.append(e)
            tier = f'price_tier={e.price_tier}' if e.price > 0 else 'FREE'
            print(f'  [{len(events)-1:02d}] {e.title} ({tier})')

        # -----------------------------------------------------------------
        # 4. USERS  (22 regular users - diverse cities, budgets, sport prefs)
        #
        # Key design choices:
        #   - Users 20 & 21 -> cold-start (no bookings at all)
        #   - Users 4 & 12  -> power users (6 bookings each)
        #   - Overlapping sport preferences -> collaborative filtering signal
        #   - Mix of cheap / mid / premium budgets across same cities
        # -----------------------------------------------------------------
        print('\nSeeding users ...')

        users_raw = [
            # idx  name                   email              city        budget     preferred_sports
            (0,  'Rahul Sharma',     'user1@gmail.com',   'Delhi',     'mid',     ['Football', 'Cricket', 'Running']),
            (1,  'Priya Patel',      'user2@gmail.com',   'Mumbai',    'cheap',   ['Running', 'Yoga', 'Swimming']),
            (2,  'Aditya Nair',      'user3@gmail.com',   'Bangalore', 'mid',     ['Cycling', 'Running', 'Basketball']),
            (3,  'Sneha Rao',        'user4@gmail.com',   'Chennai',   'premium', ['Tennis', 'Swimming', 'Athletics']),
            (4,  'Vikram Singh',     'user5@gmail.com',   'Delhi',     'premium', ['Cricket', 'Football', 'Athletics']),
            (5,  'Ananya Menon',     'user6@gmail.com',   'Bangalore', 'cheap',   ['Yoga', 'Running', 'Cycling']),
            (6,  'Rohan Gupta',      'user7@gmail.com',   'Pune',      'mid',     ['Basketball', 'Badminton', 'Running']),
            (7,  'Kavita Joshi',     'user8@gmail.com',   'Mumbai',    'mid',     ['Cricket', 'Running', 'Swimming']),
            (8,  'Arjun Reddy',      'user9@gmail.com',   'Chennai',   'cheap',   ['Tennis', 'Swimming', 'Badminton']),
            (9,  'Meera Iyer',       'user10@gmail.com',  'Bangalore', 'premium', ['Yoga', 'Cycling', 'Athletics']),
            (10, 'Siddharth Kumar',  'user11@gmail.com',  'Delhi',     'mid',     ['Football', 'Basketball', 'Running']),
            (11, 'Divya Shukla',     'user12@gmail.com',  'Pune',      'cheap',   ['Badminton', 'Running', 'Yoga']),
            (12, 'Kiran Desai',      'user13@gmail.com',  'Mumbai',    'premium', ['Cricket', 'Football', 'Basketball']),
            (13, 'Tejal Shah',       'user14@gmail.com',  'Bangalore', 'mid',     ['Running', 'Swimming', 'Cycling']),
            (14, 'Manish Verma',     'user15@gmail.com',  'Delhi',     'cheap',   ['Athletics', 'Running', 'Football']),
            (15, 'Pooja Pillai',     'user16@gmail.com',  'Chennai',   'mid',     ['Swimming', 'Tennis', 'Running']),
            (16, 'Nikhil Bose',      'user17@gmail.com',  'Pune',      'mid',     ['Basketball', 'Cricket', 'Football']),
            (17, 'Ritu Mathur',      'user18@gmail.com',  'Delhi',     'premium', ['Athletics', 'Running', 'Yoga']),
            (18, 'Gaurav Tiwari',    'user19@gmail.com',  'Mumbai',    'cheap',   ['Cricket', 'Badminton', 'Football']),
            (19, 'Shruti Kaur',      'user20@gmail.com',  'Bangalore', 'mid',     ['Cycling', 'Yoga', 'Running']),
            # cold-start users (no bookings -> tests recommendation for new users)
            (20, 'Zara Ahmed',       'user21@gmail.com',  'Chennai',   'premium', ['Tennis', 'Athletics']),
            (21, 'Dhruv Mehta',      'user22@gmail.com',  'Pune',      'cheap',   ['Badminton', 'Basketball']),
        ]

        users: list[User] = []
        for _, name, email, city, budget, sports in users_raw:
            u = make_user(name, email, 'user', city, budget, sports)
            db.session.add(u)
            users.append(u)
        db.session.commit()
        print(f'  -> {len(users)} users created (including 2 cold-start)')

        # ─────────────────────────────────────────────────────────────────
        # 5. REGISTRATIONS & PAYMENTS
        #
        # booking_map: user_index → [event_indices]
        #
        # Logic:
        #   • Mostly aligned with preferred_sports + city for recommendation signal
        #   • Some cross-city bookings for realism (people travel for events)
        #   • Some budget mismatches intentionally (impulse bookings)
        #   • Users 4 & 12 are power users (5–6 events each)
        #   • Users 20 & 21 absent (cold-start edge case)
        # ─────────────────────────────────────────────────────────────────
        print('\nSeeding registrations & payments ...')

        booking_map: dict[int, list[int]] = {
            # Rahul (Delhi, mid, Football+Cricket+Running)
            0:  [0, 3, 2, 10, 14],

            # Priya (Mumbai, cheap, Running+Yoga+Swimming)
            1:  [6, 7, 21, 24, 14],

            # Aditya (Bangalore, mid, Cycling+Running+Basketball)
            2:  [5, 7, 17, 15],

            # Sneha (Chennai, premium, Tennis+Swimming+Athletics)  ← power user 1
            3:  [20, 21, 22, 23, 24],

            # Vikram (Delhi, premium, Cricket+Football+Athletics)  ← power user 2
            4:  [0, 3, 1, 10, 11, 14],

            # Ananya (Bangalore, cheap, Yoga+Running+Cycling)
            5:  [6, 7, 5],

            # Rohan (Pune, mid, Basketball+Badminton+Running)
            6:  [15, 16, 17, 19],

            # Kavita (Mumbai, mid, Cricket+Running+Swimming)
            7:  [10, 11, 7, 21],

            # Arjun (Chennai, cheap, Tennis+Swimming+Badminton)
            8:  [20, 21, 22, 16],

            # Meera (Bangalore, premium, Yoga+Cycling+Athletics)
            9:  [6, 5, 8, 9, 24],

            # Siddharth (Delhi, mid, Football+Basketball+Running)
            10: [0, 15, 2, 17],

            # Divya (Pune, cheap, Badminton+Running+Yoga)
            11: [16, 17, 6, 19],

            # Kiran (Mumbai, premium, Cricket+Football+Basketball) ← power user 3
            12: [10, 11, 0, 15, 13, 12],

            # Tejal (Bangalore, mid, Running+Swimming+Cycling)
            13: [7, 23, 5, 8],

            # Manish (Delhi, cheap, Athletics+Running+Football)
            14: [1, 2, 4, 0],

            # Pooja (Chennai, mid, Swimming+Tennis+Running)
            15: [21, 20, 23, 7],

            # Nikhil (Pune, mid, Basketball+Cricket+Football)
            16: [15, 10, 14, 18],

            # Ritu (Delhi, premium, Athletics+Running+Yoga)
            17: [1, 2, 4, 9],

            # Gaurav (Mumbai, cheap, Cricket+Badminton+Football)
            18: [3, 10, 16, 14],

            # Shruti (Bangalore, mid, Cycling+Yoga+Running)
            19: [5, 6, 7, 8],

            # users 20 & 21 intentionally absent → cold-start
        }

        total_regs = 0
        total_payments = 0

        for user_idx, event_indices in booking_map.items():
            user = users[user_idx]
            for event_idx in event_indices:
                event = events[event_idx]
                reg = safe_register(user, event, status='confirmed')
                if reg:
                    total_regs += 1
                    if event.price > 0:
                        total_payments += 1

        # Extra randomized historical bookings across existing users/events.
        # This improves daily/weekly graph trends without creating new users.
        now_utc = datetime.utcnow()
        random_historical_target = 40
        random_historical_added = 0
        randomized_users = users[:20]  # exclude cold-start users (indices 20, 21)
        reserved_pairs = {
            (0, 8),   # Rahul + Trail Cycling reserved for pending edge case
            (5, 9),   # Ananya + Zen Yoga reserved for cancelled edge case
        }

        shuffled_users = randomized_users.copy()
        random.shuffle(shuffled_users)

        for user in shuffled_users:
            if random_historical_added >= random_historical_target:
                break

            candidate_events = events.copy()
            random.shuffle(candidate_events)

            # 1 to 3 additional bookings per user if available
            max_for_user = random.randint(1, 3)
            added_for_user = 0

            for event in candidate_events:
                if random_historical_added >= random_historical_target or added_for_user >= max_for_user:
                    break

                if event.seats_remaining <= 0:
                    continue

                if Registration.query.filter_by(user_id=user.id, event_id=event.id).first():
                    continue

                user_idx = users.index(user)
                event_idx = events.index(event)
                if (user_idx, event_idx) in reserved_pairs:
                    continue

                random_days_ago = random.randint(0, 29)
                random_minutes = random.randint(0, 1439)
                created_at = now_utc - timedelta(days=random_days_ago, minutes=random_minutes)

                reg = safe_register(user, event, status='confirmed', created_at=created_at)
                if reg:
                    random_historical_added += 1
                    total_regs += 1
                    if event.price > 0:
                        total_payments += 1
                    added_for_user += 1

        print(
            f'  -> Added {random_historical_added} randomized confirmed bookings '
            f'with created_at spread over last 30 days'
        )

        # ─────────────────────────────────────────────────────────────────
        # 6. EDGE CASES
        # ─────────────────────────────────────────────────────────────────

        # Edge case A: PENDING (unpaid) registration
        # User 0 (Rahul) starts checkout for the premium Trail Cycling event
        # but never completes payment.
        trail_cycling = events[8]   # Trail Cycling – Coorg Edition  (₹4500)
        rahul = users[0]
        existing_tc = Registration.query.filter_by(
            user_id=rahul.id, event_id=trail_cycling.id
        ).first()
        if not existing_tc and trail_cycling.seats_remaining > 0:
            pending_reg = create_registration(rahul.id, trail_cycling.id, status='pending')
            db.session.add(pending_reg)
            db.session.commit()
            # Payment order created but not paid
            incomplete_payment = create_payment(pending_reg.id, trail_cycling.price, paid=False)
            db.session.add(incomplete_payment)
            db.session.commit()
            print('  -> Edge case A: Pending (unpaid) booking - Rahul / Trail Cycling')

        # Edge case B: CANCELLED registration
        # Ananya (user 5) had registered for the Zen Yoga Retreat but cancelled.
        zen_yoga = events[9]   # Zen Yoga & Meditation Retreat  (₹2999, past)
        ananya = users[5]
        existing_zy = Registration.query.filter_by(
            user_id=ananya.id, event_id=zen_yoga.id
        ).first()
        if not existing_zy:
            cancelled_reg = create_registration(ananya.id, zen_yoga.id, status='cancelled')
            db.session.add(cancelled_reg)
            db.session.commit()
            print('  -> Edge case B: Cancelled registration - Ananya / Zen Yoga Retreat')

        # ─────────────────────────────────────────────────────────────────
        # 7. SUMMARY
        # ─────────────────────────────────────────────────────────────────
        print('\n' + '=' * 58)
        print('DONE  Seeding complete!')
        print('=' * 58)
        print(f'  Users    : 1 admin + {len(organizers)} organizers + {len(users)} regular users')
        print(f'  Events   : {len(events)} (across 5 sport categories & 5 cities)')
        print(f'  Bookings : {total_regs} confirmed registrations')
        print(f'  Payments : {total_payments} paid transactions')
        print(f'  Edge cases: 2 cold-start users, 1 pending payment, 1 cancellation  ')
        print('-' * 58)
        print('  Password for ALL accounts : 123456')
        print('  Admin  : admin@livesports.in')
        print('  Orgs   : org1@gmail.com ... org5@gmail.com')
        print('  Users  : user1@gmail.com ... user22@gmail.com')
        print('=' * 58)


if __name__ == '__main__':
    seed_database()