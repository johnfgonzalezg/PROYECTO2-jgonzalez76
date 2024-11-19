from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from models.ingredient import Ingredient
from models.ingredient_type import IngredientType

ingredient_bp = Blueprint('ingredient', __name__)


@ingredient_bp.route('/', methods = ['GET'], endpoint = 'index')
def index():
    ingredients = db.session.query(Ingredient, IngredientType).join(IngredientType, Ingredient.id_ingredient_type == IngredientType.id).all()
    print(ingredients)
    return render_template('ingredient/index.html', ingredients = ingredients)


@ingredient_bp.route('/create', methods = ['GET', 'POST'], endpoint = 'create')
def create():
    if request.method == 'POST':
        id_ingredient_type = request.form['ingredient_type']
        name = request.form['name']
        calories = request.form['calories']
        price = request.form['price']
        is_vegetarian = request.form.get('is_vegetarian') == 'True'
        quantity = request.form['quantity']
        ingredient = Ingredient(id_ingredient_type = id_ingredient_type, name = name, calories = calories, price = price, is_vegetarian = is_vegetarian, quantity = quantity)
        db.session.add(ingredient)
        db.session.commit()
        return redirect(url_for('ingredient.index'))
    ingredient_types = IngredientType.query.all()
    return render_template('ingredient/create.html', ingredient_types = ingredient_types)


@ingredient_bp.route('/edit/<int:id>', methods = ['GET', 'POST'], endpoint = 'edit')
def edit(id):
    ingredient = Ingredient.query.get_or_404(id)
    if request.method == 'POST':
        ingredient.id_ingredient_type = request.form['ingredient_type']
        ingredient.name = request.form['name']
        ingredient.calories = request.form['calories']
        ingredient.price = request.form['price']
        ingredient.is_vegetarian = request.form.get('is_vegetarian') == 'True'
        ingredient.quantity = request.form['quantity']
        db.session.commit()
        return redirect(url_for('ingredient.index'))
    ingredient_types = IngredientType.query.all()
    return render_template('ingredient/edit.html', ingredient = ingredient, ingredient_types = ingredient_types)

@ingredient_bp.route('/delete/<int:id>', methods = ['POST'], endpoint = 'delete')
def delete(id):
    ingredient = Ingredient.query.get_or_404(id)
    db.session.delete(ingredient)
    db.session.commit()
    return redirect(url_for('ingredient.index'))

