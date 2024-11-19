from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from models.product import Product
from models.product_type import ProductType
from models.ingredient import Ingredient
from models.product_ingredient import ProductIngredient

product_bp = Blueprint('product', __name__)


@product_bp.route('/', methods = ['GET'], endpoint = 'index')
def index():
    products = db.session.query(Product, ProductType).join(ProductType, Product.id_product_type == ProductType.id).all()
    return render_template('product/index.html', products = products)


@product_bp.route('/create', methods = ['GET', 'POST'], endpoint = 'create')
def create():
    products = Product.query.count()
    if products >= 4:
        raise ValueError('Ya existen cuantro productos en el menú')
    elif request.method == 'POST':
        id_product_type = request.form['product_type']
        name = request.form['name']
        calories = request.form['calories']
        cost = request.form['cost']
        public_price = request.form['public_price']
        profitability = request.form['profitability']
        ingredient_1 = request.form['ingredient_1']
        ingredient_2 = request.form['ingredient_2']
        ingredient_3 = request.form['ingredient_3']
        product = Product(id_product_type = id_product_type, name = name, calories = calories, cost = cost, public_price = public_price, profitability = profitability)
        db.session.add(product)
        db.session.flush()
        product_ingredient_1 = ProductIngredient(id_product = product.id, id_ingredient = ingredient_1)
        product_ingredient_2 = ProductIngredient(id_product = product.id, id_ingredient = ingredient_2)
        product_ingredient_3 = ProductIngredient(id_product = product.id, id_ingredient = ingredient_3)
        db.session.add(product_ingredient_1)
        db.session.add(product_ingredient_2)
        db.session.add(product_ingredient_3)
        db.session.commit()
        return redirect(url_for('product.index'))
    product_types = ProductType.query.all()
    print(product_types)
    ingredients = Ingredient.query.all()
    return render_template('product/create.html', product_types = product_types, ingredients = ingredients)


@product_bp.route('/edit/<int:id>', methods = ['GET', 'POST'], endpoint = 'edit')
def edit(id):
    product = Product.query.get_or_404(id)
    product_ingredients = ProductIngredient.query.filter_by(id_product=id).all()
    for product_ingredient in product_ingredients:
        print(f'id_product: {product_ingredient.id_product}, id_ingredient: {product_ingredient.id_ingredient}')
    if request.method == 'POST':
        db.session.query(ProductIngredient).filter(ProductIngredient.id_product == id).delete()
        product.id_ingredient_type = request.form['product_type']
        product.name = request.form['name']
        product.calories = request.form['calories']
        product.cost = request.form['cost']
        product.public_price = request.form['public_price']
        product.profitability = request.form['profitability']
        ingredient_1 = request.form['ingredient_1']
        ingredient_2 = request.form['ingredient_2']
        ingredient_3 = request.form['ingredient_3']
        product_ingredient_1 = ProductIngredient(id_product = product.id, id_ingredient = ingredient_1)
        product_ingredient_2 = ProductIngredient(id_product = product.id, id_ingredient = ingredient_2)
        product_ingredient_3 = ProductIngredient(id_product = product.id, id_ingredient = ingredient_3)
        db.session.add(product_ingredient_1)
        db.session.add(product_ingredient_2)
        db.session.add(product_ingredient_3)
        db.session.commit()
        return redirect(url_for('product.index'))
    product_types = ProductType.query.all()
    ingredients = Ingredient.query.all()
    return render_template('product/edit.html', product = product, product_types = product_types, ingredients = ingredients, product_ingredients = product_ingredients)

@product_bp.route('/delete/<int:id>', methods = ['POST'], endpoint = 'delete')
def delete(id):
    ProductIngredient.query.filter_by(id_product = id).delete()
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product.index'))

