from app import app, db
from seed_data import seed_database

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_database()
    print("Database has been reset and seeded.")
