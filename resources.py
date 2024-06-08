from flask import request
from flask_restful import Resource
from models import User, Item, Bid
from schemas import UserSchema, ItemSchema, BidSchema
from db import db
from flasgger import swag_from

user_schema = UserSchema()
users_schema = UserSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
bid_schema = BidSchema()
bids_schema = BidSchema()

class UserResource(Resource):
    @swag_from({
        'responses': {
            201: {
                'description': 'User created',
                'schema': UserSchema
            }
        }
    })
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
    @swag_from({
        'responses': {
            201: {
                'description': 'Item created',
                'schema': ItemSchema
            }
        }
    })
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

    @swag_from({
        'responses': {
            200: {
                'description': 'List of items',
                'schema': ItemSchema(many=True)
            }
        }
    })
    def get(self):
        items = Item.query.all()
        return items_schema.dump(items), 200

class BidResource(Resource):
    @swag_from({
        'responses': {
            201: {
                'description': 'Bid created',
                'schema': BidSchema
            },
            400: {
                'description': 'Bid must be higher than current highest bid'
            }
        }
    })
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
    @swag_from({
        'responses': {
            200: {
                'description': 'Item details',
                'schema': ItemSchema
            },
            404: {
                'description': 'Item not found'
            }
        }
    })
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return item_schema.dump(item), 200
