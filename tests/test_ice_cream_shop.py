import unittest
from datetime import datetime
from app import app
from db import db
from models.product import Product
from models.product_ingredient import ProductIngredient
from models.ingredient import Ingredient
from models.product_type import ProductType
from models.daily_sell import DailySells

class IceCreamShopTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        product_type = ProductType(id=1, type='Type1')
        ingredient = Ingredient(id=1, id_ingredient_type=1, name='Test Ingredient', calories=100, price=5.0, is_vegetarian=True, quantity=10)
        product = Product(id=1, id_product_type=1, name='Test Product', public_price=20.0)
        product_ingredient = ProductIngredient(id_product=1, id_ingredient=1)
        daily_sell = DailySells(sell_date=datetime.today().date(), total_sell_value=0)

        db.session.add(product_type)
        db.session.add(ingredient)
        db.session.add(product)
        db.session.add(product_ingredient)
        db.session.add(daily_sell)
        db.session.commit()

    def test_calculate_calories(self):
        with app.app_context():
            response = self.app.get('/product/calculate_calories/1')
            self.assertEqual(response.status_code, 302)  # Redirección

    def test_calculate_cost(self):
        with app.app_context():
            response = self.app.get('/product/calculate_cost/1')
            self.assertEqual(response.status_code, 302)  # Redirección

    def test_calculate_profitability(self):
        with app.app_context():
            response = self.app.get('/product/calculate_profitability/1')
            self.assertEqual(response.status_code, 302)  # Redirección

    def test_most_profitable_product(self):
        with app.app_context():
            response = self.app.get('/product/most_profitable_product')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Product', response.data)

    def test_sold_product(self):
        with app.app_context():
            response = self.app.post('/sold_product', data={'sell_product': 1})
            self.assertEqual(response.status_code, 302)  # Redirección

if __name__ == '__main__':
    unittest.main()
