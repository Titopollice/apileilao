import unittest
from flask import Flask
from flask_testing import TestCase
from app import app, db
from models import User, Item, Bid

class MyTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()
        self.user1 = User(username='testuser', email='test@example.com', password='password')
        self.item1 = Item(title='Test Item', description='This is a test item', start_bid=10.0)
        db.session.add(self.user1)
        db.session.add(self.item1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
        response = self.client.post('/users', json={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['username'], 'newuser')

    def test_item_creation(self):
        response = self.client.post('/items', json={
            'title': 'New Item',
            'description': 'Description of new item',
            'start_bid': 20.0
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['title'], 'New Item')

    def test_get_items(self):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['title'], 'Test Item')

    def test_place_bid(self):
        response = self.client.post('/bids', json={
            'amount': 15.0,
            'user_id': self.user1.id,
            'item_id': self.item1.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['amount'], 15.0)

if __name__ == '__main__':
    unittest.main()
