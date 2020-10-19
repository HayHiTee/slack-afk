from app import db
from datetime import datetime, timedelta


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)
    access_token = db.Column(db.String(180), unique=False, nullable=False)
    scope = db.Column(db.String(180), unique=False, nullable=True)
    auth_user_id = db.Column(db.String(100), unique=False, nullable=True)
    team_id = db.Column(db.String(180), unique=False, nullable=True)
    team_name = db.Column(db.String(180), unique=False, nullable=True)
    date_created = db.Column(db.DateTime, index=False, unique=False, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return '<User %r>' % self.username
