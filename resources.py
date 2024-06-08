from flask import request
from flask_restful import Resource
from models import User, Item, Bid
from schemas import UserSchema, ItemSchema, BidSchema
from db import db

user_schema = UserSchema()
users_schema = UserSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
bid_schema = BidSchema()
bids_schema = BidSchema(many=True)

class UserResource(Resource):
    def post(self):
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201

class ItemResource(Resource):
    def post(self):
        data = request.get_json()
        new_item = Item(
            title=data['title'],
            description=data['description'],
            start_bid=data['start_bid']
        )
        db.session.add(new_item)
        db.session.commit()
        return item_schema.dump(new_item), 201

    def get(self):
        items = Item.query.all()
        return items_schema.dump(items), 200

class BidResource(Resource):
    def post(self):
        data = request.get_json()
        item = Item.query.get(data['item_id'])
        if data['amount'] <= item.highest_bid:
            return {'message': 'Bid must be higher than current highest bid.'}, 400
        new_bid = Bid(
            amount=data['amount'],
            user_id=data['user_id'],
            item_id=data['item_id']
        )
        item.highest_bid = new_bid.amount
        item.highest_bidder_id = new_bid.user_id
        db.session.add(new_bid)
        db.session.commit()
        return bid_schema.dump(new_bid), 201

class ItemDetailResource(Resource):
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return item_schema.dump(item), 200
