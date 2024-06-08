import os
from flask import Flask, jsonify
from flask_restful import Api
from flasgger import Swagger
from db import db
from schemas import ma
from resources import UserResource, ItemResource, BidResource, ItemDetailResource
from swagger import swaggerui_blueprint, SWAGGER_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:kHgXOUGbdIjSJNhZoShLnObQZvfkkVvA@monorail.proxy.rlwy.net:30339/railway')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

api = Api(app)

api.add_resource(UserResource, '/users')
api.add_resource(ItemResource, '/items')
api.add_resource(BidResource, '/bids')
api.add_resource(ItemDetailResource, '/items/<int:item_id>')

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Auction API"}), 200

# Configuração do Flasgger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Auction API",
        "description": "API for managing auctions",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Criação das tabelas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
