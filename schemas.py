from flask_marshmallow import Marshmallow
from models import User, Item, Bid

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item

class BidSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bid
