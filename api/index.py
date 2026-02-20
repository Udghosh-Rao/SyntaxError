import sys
import os
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app import create_app

app = create_app()

# Export app for Vercel
@app.route('/', methods=['GET'])
def home():
    return {"status": "SyntaxError API running", "version": "1.0"}

if __name__ == '__main__':
    app.run()
