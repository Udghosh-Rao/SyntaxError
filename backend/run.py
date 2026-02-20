#!/usr/bin/env python
import os
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
    app.run(debug=True, host='0.0.0.0', port=5000)
