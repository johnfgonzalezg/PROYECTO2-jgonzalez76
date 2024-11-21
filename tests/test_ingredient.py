import unittest
from app import app
from db import db
from models.ingredient import Ingredient
from models.ingredient_type import IngredientType

class IngredientTests(unittest.TestCase):
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
        ingredient_type = IngredientType(type='Type1')
        db.session.add(ingredient_type)
        db.session.flush()
        ingredient = Ingredient(id_ingredient_type=1, name='Healthy Ingredient', calories=50, price=10.0, is_vegetarian=True, quantity=10)
        db.session.add(ingredient)
        db.session.commit()

    def test_is_healthy_sano(self):
        with app.app_context():
            ingredient = Ingredient.query.first()
            response = self.app.get(f'/ingredient/its_healthy/{ingredient.id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'El ingrediente es sano', response.data)

    def test_is_healthy_no_sano(self):
        with app.app_context():
            ingredient = Ingredient(id_ingredient_type=1, name='Unhealthy Ingredient', calories=150, price=10.0, is_vegetarian=False, quantity=10)
            db.session.add(ingredient)
            db.session.commit()
            
            response = self.app.get(f'/ingredient/its_healthy/{ingredient.id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'El ingrediente no es sano', response.data)

    def test_supply(self):
        with app.app_context():
            ingredient = Ingredient.query.first()
            self.app.get(f'/ingredient/supply/{ingredient.id}')
            self.assertEqual(ingredient.quantity, 15)  # assuming supply adds 5 to quantity

if __name__ == '__main__':
    unittest.main()
