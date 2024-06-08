from datetime import datetime, timedelta
from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    bids = db.relationship('Bid', backref='user', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    start_bid = db.Column(db.Float, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=1))
    highest_bid = db.Column(db.Float, nullable=False, default=0.0)
    highest_bidder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    bids = db.relationship('Bid', backref='item', lazy=True)

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
