from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from models.product import Product
from models.product_type import ProductType
from models.ingredient import Ingredient
from models.product_ingredient import ProductIngredient

product_bp = Blueprint('product', __name__)

@product_bp.route('/', methods=['GET'], endpoint='index')
def index():
    products = db.session.query(Product, ProductType).join(ProductType, Product.id_product_type == ProductType.id).all()
    error_message = request.args.get('error_message')
    if error_message:
        print('error_message: ' + error_message)
    return render_template('product/index.html', products = products, error_message = error_message)

@product_bp.route('/create', methods=['GET', 'POST'], endpoint='create')
def create():
    products = Product.query.count()
    try:
        if products >= 4:
            raise ValueError('Ya existen cuatro productos en el menú')
        elif request.method == 'POST':
            id_product_type = request.form['product_type']
            name = request.form['name']
            public_price = request.form['public_price']
            cup_type = request.form['cup_type']
            ingredient_1 = request.form['ingredient_1']
            ingredient_2 = request.form['ingredient_2']
            ingredient_3 = request.form['ingredient_3']
            product = Product(id_product_type=id_product_type, name=name, public_price=public_price, cup_type=cup_type)
            db.session.add(product)
            db.session.flush()
            product_ingredient_1 = ProductIngredient(id_product=product.id, id_ingredient=ingredient_1)
            product_ingredient_2 = ProductIngredient(id_product=product.id, id_ingredient=ingredient_2)
            product_ingredient_3 = ProductIngredient(id_product=product.id, id_ingredient=ingredient_3)
            db.session.add(product_ingredient_1)
            db.session.add(product_ingredient_2)
            db.session.add(product_ingredient_3)
            db.session.commit()
            calculate_calories(product.id)
            calculate_cost(product.id)
            calculate_profitability(product.id)
            db.session.commit()
            return redirect(url_for('product.index'))
    except ValueError as e:
        print('Error: ' + str(e))
        error_message = str(e)
        return redirect(url_for('product.index', error_message = error_message))
    product_types = ProductType.query.all()
    ingredients = Ingredient.query.all()
    return render_template('product/create.html', product_types=product_types, ingredients=ingredients)

@product_bp.route('/edit/<int:id>', methods=['GET', 'POST'], endpoint='edit')
def edit(id):
    product = Product.query.get_or_404(id)
    product_ingredients = ProductIngredient.query.filter_by(id_product=id).all()
    for product_ingredient in product_ingredients:
        print(f'id_product: {product_ingredient.id_product}, id_ingredient: {product_ingredient.id_ingredient}')
    if request.method == 'POST':
        db.session.query(ProductIngredient).filter(ProductIngredient.id_product == id).delete()
        product.id_ingredient_type = request.form['product_type']
        product.name = request.form['name']
        product.public_price = request.form['public_price']
        product.cup_type = request.form['cup_type']
        ingredient_1 = request.form['ingredient_1']
        ingredient_2 = request.form['ingredient_2']
        ingredient_3 = request.form['ingredient_3']
        product_ingredient_1 = ProductIngredient(id_product=product.id, id_ingredient=ingredient_1)
        product_ingredient_2 = ProductIngredient(id_product=product.id, id_ingredient=ingredient_2)
        product_ingredient_3 = ProductIngredient(id_product=product.id, id_ingredient=ingredient_3)
        db.session.add(product_ingredient_1)
        db.session.add(product_ingredient_2)
        db.session.add(product_ingredient_3)
        db.session.commit()
        calculate_calories(product.id)
        calculate_cost(product.id)
        calculate_profitability(product.id)
        return redirect(url_for('product.index'))
    product_types = ProductType.query.all()
    ingredients = Ingredient.query.all()
    return render_template('product/edit.html', product=product, product_types=product_types, ingredients=ingredients, product_ingredients=product_ingredients)

@product_bp.route('/delete/<int:id>', methods=['POST'], endpoint='delete')
def delete(id):
    ProductIngredient.query.filter_by(id_product=id).delete()
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product.index'))

@product_bp.route('/calculate_calories/<int:id>', methods=['GET'], endpoint='calculate_calories')
def calculate_calories(id):
    product = Product.query.get_or_404(id)
    product_ingredients = ProductIngredient.query.filter_by(id_product=id).all()

    calories = 0
    for product_ingredient in product_ingredients:
        ingredient = Ingredient.query.get(product_ingredient.id_ingredient)
        calories += ingredient.calories
        print('calories 1: ' + str(calories))

    if product.id_product_type == 1:
        product.calories = calories * 0.95
        print('calories 2: ' + str(product.calories))
    elif product.id_product_type == 2:
        product.calories = calories + 200
        print('calories 3: ' + str(product.calories))

    print('calories 4: ' + str(product.calories))
    db.session.commit()
    return redirect(url_for('product.index'))

@product_bp.route('/calculate_cost/<int:id>', methods=['GET'], endpoint='calculate_cost')
def calculate_cost(id):
    product = Product.query.get_or_404(id)
    product_ingredients = ProductIngredient.query.filter_by(id_product=id).all()

    cost = 0
    for product_ingredient in product_ingredients:
        ingredient = Ingredient.query.get(product_ingredient.id_ingredient)
        cost += ingredient.price

    if product.id_product_type == 1:
        product.cost = cost
    elif product.id_product_type == 2:
        cost_plastic_cups = 500
        product.cost = cost + cost_plastic_cups

    db.session.commit()
    return redirect(url_for('product.index'))

@product_bp.route('/calculate_profitability/<int:id>', methods=['GET'], endpoint='calculate_profitability')
def calculate_profitability(id):
    product = Product.query.get_or_404(id)
    product.profitability = product.public_price - product.cost
    db.session.commit()
    return redirect(url_for('product.index'))
