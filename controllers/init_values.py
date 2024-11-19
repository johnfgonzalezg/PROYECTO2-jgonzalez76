from db import db
from models.ingredient_type import IngredientType
from models.product_type import ProductType
from models.product_ingredient import ProductIngredient
from models.product import Product
from models.ingredient import Ingredient

def insert_initial_values(app) -> None:
    with app.app_context():
        if not IngredientType.query.first():
            base = IngredientType(type = 'Base')
            complement = IngredientType(type = 'Complemento')
            db.session.add(base)
            db.session.add(complement)
        
        if not ProductType.query.first():
            cup = ProductType(type = 'Copa')
            milk_shake = ProductType(type = 'Malteada')
            db.session.add(cup)
            db.session.add(milk_shake)
        
        db.session.commit()
        

        strawberry_icecream = Ingredient(id_ingredient_type = 1, name = 'Helado de fresa', calories=50, price=1200, is_vegetarian=False, quantity=5, flavor='Fresa')
        choco_chips = Ingredient(id_ingredient_type=2, name='Chispas de chocolate', calories=20, price=500, is_vegetarian=False, quantity=5, flavor='Chocolate')
        japanese_penut = Ingredient(id_ingredient_type=2, name='Maní japonés', calories=20, price=500, is_vegetarian=True, quantity=4)
        vanila_icecream = Ingredient(id_ingredient_type=1, name='Helado de vainilla', calories=3, price=1200, is_vegetarian=False, quantity=5, flavor='Vainilla')
        various_fruits = Ingredient(id_ingredient_type=1, name='Frutas varias', calories=30, price=800, is_vegetarian=True, quantity=5,  flavor='Frutas')
        nut = Ingredient(id_ingredient_type=2, name='Nuez', calories=25, price=600, is_vegetarian=True, quantity=3)
        cereals = Ingredient(id_ingredient_type=2, name='Cereales', calories=15, price=400, is_vegetarian=True, quantity=4)
        caramel_syrop = Ingredient(id_ingredient_type=2, name='Sirope de caramelo', calories=10, price=200, is_vegetarian=True, quantity=2)
        ingredients = [
            strawberry_icecream,
            choco_chips,
            japanese_penut,
            vanila_icecream,
            various_fruits,
            nut,
            cereals,
            caramel_syrop
        ]

        strawberry_samurai = Product(id_product_type=1, name='Samurai de fresas', calories=900, cost=10000, public_price=12500.0, profitability=3400, cup_type='Vaso de plástico')
        chocospacial_milkshake = Product(id_product_type=2, name='Malteada chocoespacial', calories=850, cost=6500, public_price=12000.0, profitability=5000)
        fruits_cup = Product(id_product_type=1, name='Copa de frutas', calories=600, cost=8000, public_price=10800.0, profitability=1900, cup_type='Vaso de frutas')

        products = [
            strawberry_samurai,
            chocospacial_milkshake,
            fruits_cup
        ]

        product_ingredients = [
            ProductIngredient(id_product=1, id_ingredient=1),
            ProductIngredient(id_product=1, id_ingredient=2),
            ProductIngredient(id_product=1, id_ingredient=3),
            ProductIngredient(id_product=2, id_ingredient=1),
            ProductIngredient(id_product=2, id_ingredient=2),
            ProductIngredient(id_product=2, id_ingredient=3),
            ProductIngredient(id_product=3, id_ingredient=4),
            ProductIngredient(id_product=3, id_ingredient=6),
            ProductIngredient(id_product=3, id_ingredient=7),

        ]
        db.session.bulk_save_objects(ingredients)
        db.session.bulk_save_objects(products)
        db.session.bulk_save_objects(product_ingredients)

        
        db.session.commit()
