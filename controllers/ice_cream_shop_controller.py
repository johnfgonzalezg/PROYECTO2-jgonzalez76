from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from models.ingredient import Ingredient
from models.product import Product
from models.product_ingredient import ProductIngredient
from models.ingredient_type import IngredientType
from models.daily_sell import DailySells
from datetime import datetime
from decimal import Decimal


ice_cream_shop_bp = Blueprint('ice_cream_shop', __name__)

@ice_cream_shop_bp.route('/', methods=['GET'], endpoint='index')
def index():
    return render_template('index.html')

@ice_cream_shop_bp.route('/most_profitable_product', methods=['GET'], endpoint='most_profitable_product')
def most_profitable_product():
    most_profitable_product = Product.query.order_by(Product.profitability.desc()).first()
    return render_template('most_profitable_product.html', product = most_profitable_product)

@ice_cream_shop_bp.route('/daily_sails', methods=['GET'], endpoint='daily_sails')
def daily_sails():
    today = datetime.today().date()
    daily_sail = DailySells.query.filter_by(sell_date = today).first()
    return render_template('daily_sails.html', daily_sail = daily_sail)

@ice_cream_shop_bp.route('/sold_product', methods=['GET', 'POST'], endpoint='sold_product')
def sold_product():
    ingredients = Ingredient.query.all()
    products = Product.query.all()
    if request.method == 'POST':
        id_product = request.form['sell_product']
        print('id_product: ' + str(id_product))
        sold_product = Product.query.get_or_404(id_product)
        product_ingredients = ProductIngredient.query.filter_by(id_product=id_product).all()
        id_ingredients = [pi.id_ingredient for pi in product_ingredients]
        print(f'id_ingredients: {id_ingredients}')
        ingredients_product = Ingredient.query.filter(Ingredient.id.in_(id_ingredients)).all()
        have_stock = False
        for ingredient in ingredients_product:
            print(f'Checking stock for ingredient: {ingredient}')
            have_stock = check_stock(ingredient)
            if not have_stock:
                raise ValueError('No hay suficientes existencias de ingredientes para preparar el producto')
            
        if have_stock:
            for id_ingredient in id_ingredients:
                print(f'id_ingredient to subtract: {id_ingredient}')
                subtrack_stock(ingredients, id_ingredient)
            actual_date = datetime.today().date()
            daily_sell = DailySells.query.filter_by(sell_date=actual_date).first()
            if not daily_sell:
                sell_date = actual_date
                total_sell_value = sold_product.public_price
                daily_sell = DailySells(sell_date=sell_date, total_sell_value=total_sell_value)
                db.session.add(daily_sell)
                db.session.commit()
            else:
                daily_sell.total_sell_value += sold_product.public_price
                db.session.commit()
        return redirect(url_for('index'))
    return render_template('sold_product.html', products=products)


def check_stock(product_ingredient: Ingredient) -> bool:
        """
            Método que recible una lista de ingredientes (las de cada producto) y valida hay existencias suficientes de dichos ingredientes 
            en el inventario de la heladería
            **Parámentros
                Entrada:
                    - lstIngredients(list): Lista de ingredientes que se van a validar en el inventario
                Salida:
                    - (bool): Retorna True si existe el ingrediente y además suficiente cantidad en el inventario, False en caso contrario
        """
        ingredient_types = IngredientType.query.all()
        ingredients = Ingredient.query.all()
        for ingredient in ingredients:
            if ingredient.name == product_ingredient.name:
                if ingredient.id_ingredient_type == 1:
                    if ingredient.quantity >= 1.0:
                        return True
                    else: 
                        return False
                elif ingredient.id_ingredient_type == 2:
                    if ingredient.quantity >= 0.2:
                        return True
                    else:
                        return False
        return False
def subtrack_stock(ingredients_inventory: list, id_ingredient: int) -> None:
        """
            Método que recible una lista de ingredientes (las de cada producto) y resta la cantidad necesaria para preparar y vender un producto 
            determinado
            **Parámentros
                Entrada:
                    - lstIngredients(list): Lista de ingredientes que se van a modificar en el inventario
        """
        for ingredient in ingredients_inventory:
            if id_ingredient == ingredient.id:
                if ingredient.id_ingredient_type == 1:
                    ingredient.quantity = ingredient.quantity - Decimal(1.0)
                elif ingredient.id_ingredient_type == 2:
                    ingredient.quantity = ingredient.quantity - Decimal(0.2)
                db.session.commit()