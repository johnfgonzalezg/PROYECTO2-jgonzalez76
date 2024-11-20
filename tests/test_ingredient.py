import unittest
from app import app
from db import db
from models.ingredient import Ingredient, IngredientType

class IngredientTests(unittest.TestCase):
    
    def create_test_data(self):
        ingredient_type = IngredientType(id=1, type='Type1')
        ingredient = Ingredient(id_ingredient_type=1, name='Test Ingredient', calories=50, price=10.0, is_vegetarian=True, quantity=10)
        db.session.add(ingredient_type)
        db.session.add(ingredient)
        db.session.commit()

    def test_is_healthy(self):
        with app.app_context():
            ingredient = Ingredient.query.first()
            response = self.app.get(f'/ingredient/its_healthy/{ingredient.id}')
            self.assertEqual(response.status_code, 302)  # Redirección
            self.assertIn(b'El ingrediente es sano', response.data)

    def test_supply(self):
        with app.app_context():
            ingredient = Ingredient.query.first()
            self.app.get(f'/ingredient/supply/{ingredient.id}')
            self.assertEqual(ingredient.quantity, 15)

if __name__ == '__main__':
    unittest.main()
