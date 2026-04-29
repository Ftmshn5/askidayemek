from app import app, db
from seed_data import seed_database

with app.app_context():
    db.create_all()
    seed_database()
    print("Database initialized and seeded.")
