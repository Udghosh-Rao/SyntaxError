#!/usr/bin/env python
import os
from dotenv import load_dotenv

# Load .env BEFORE anything else reads os.getenv()
load_dotenv()

from app import create_app, db
from app.models import User, Event, Registration, Payment

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Event': Event, 'Registration': Registration, 'Payment': Payment}

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Database tables ensured.')
    app.run(debug=True, host='0.0.0.0', port=8000)