from app import app
from db import db

@app.before_first_request
def create_all_tables():
    db.create_all()

db.init_app(app)