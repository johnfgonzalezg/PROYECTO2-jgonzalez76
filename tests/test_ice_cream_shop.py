import unittest
from datetime import datetime
from app import app
from db import db
from models.ingredient import Ingredient
from models.ingredient_type import IngredientType
from models.product import Product
from models.product_ingredient import ProductIngredient
from models.product_type import ProductType
from models.daily_sells import DailySells

class IceCreamShopTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Utiliza una base de datos en memoria
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        # Crear un tipo de ingrediente
        ingredient_type = IngredientType(type='Test Ingredient Type')
        db.session.add(ingredient_type)
        db.session.flush()  # Asegúrate de que ingredient_type.id esté disponible para usarlo en ingredient

        # Crear un tipo de producto
        product_type = ProductType(type='Test Product Type')
        db.session.add(product_type)
        db.session.flush()  # Asegúrate de que product_type.id esté disponible para usarlo en product

        # Crear un ingrediente
        ingredient = Ingredient(id_ingredient_type=ingredient_type.id, name='Test Ingredient', calories=100, price=5.0, is_vegetarian=True, quantity=10)
        db.session.add(ingredient)
        db.session.flush()  # Asegúrate de que ingredient.id esté disponible para usarlo en product_ingredient

        # Crear un producto
        product = Product(id_product_type=product_type.id, name='Test Product', public_price=20.0)
        db.session.add(product)
        db.session.flush()  # Asegúrate de que product.id esté disponible para usarlo en product_ingredient

        # Crear un product_ingredient
        product_ingredient = ProductIngredient(id_product=product.id, id_ingredient=ingredient.id)
        db.session.add(product_ingredient)
        
        # Crear una venta diaria
        daily_sell = DailySells(sell_date=datetime.today().date(), total_sell_value=0)
        db.session.add(daily_sell)

        # Confirmar todos los cambios
        db.session.commit()

    def test_calculate_calories(self):
        with app.app_context():
            response = self.app.get('/product/calculate_calories/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            product = db.session.get(Product, 1)
            self.assertIsNotNone(product.calories)

    def test_calculate_cost(self):
        with app.app_context():
            response = self.app.get('/product/calculate_cost/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            product = db.session.get(Product, 1)
            self.assertIsNotNone(product.cost)

    def test_calculate_profitability(self):
        with app.app_context():
            response = self.app.get('/product/calculate_profitability/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            product = db.session.get(Product, 1)
            self.assertIsNotNone(product.profitability)

    def test_most_profitable_product(self):
        with app.app_context():
            response = self.app.get('/most_profitable_product', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test Product'.encode('utf-8'), response.data)

    def test_sold_product_success(self):
        with app.app_context():
            ingredient = Ingredient.query.first()
            ingredient.quantity = 10  # Ensure there's enough stock
            db.session.commit()

            response = self.app.post('/sold_product', data={'sell_product': 1}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('¡Vendido!'.encode('utf-8'), response.data)

    def test_sold_product_insufficient_stock(self):
        with app.app_context():
            ingredient = Ingredient.query.first()
            ingredient.quantity = 0  # Ensure there's insufficient stock
            db.session.commit()

            response = self.app.post('/sold_product', data={'sell_product': 1}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('¡Oh no! Nos hemos quedado sin Test Ingredient'.encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main()
