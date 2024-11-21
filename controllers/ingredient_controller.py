from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db
from models.ingredient import Ingredient
from models.ingredient_type import IngredientType

ingredient_bp = Blueprint('ingredient', __name__)

@ingredient_bp.route('/', methods=['GET'], endpoint='index')
def index():
    ingredients = db.session.query(Ingredient, IngredientType).join(IngredientType, Ingredient.id_ingredient_type == IngredientType.id).all()
    its_healthy = request.args.get('its_healthy')
    return render_template('ingredient/index.html', ingredients=ingredients, its_healthy = its_healthy)

@ingredient_bp.route('/create', methods=['GET', 'POST'], endpoint='create')
def create():
    if request.method == 'POST':
        try:
            id_ingredient_type = request.form['ingredient_type']
            name = request.form['name']
            calories = request.form['calories']
            price = request.form['price']
            is_vegetarian = request.form.get('is_vegetarian') == 'True'
            quantity = request.form['quantity']
            ingredient = Ingredient(id_ingredient_type=id_ingredient_type, name=name, calories=calories, price=price, is_vegetarian=is_vegetarian, quantity=quantity)
            db.session.add(ingredient)
            db.session.commit()
            return redirect(url_for('ingredient.index'))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('ingredient.create'))
    ingredient_types = IngredientType.query.all()
    return render_template('ingredient/create.html', ingredient_types=ingredient_types)

@ingredient_bp.route('/edit/<int:id>', methods=['GET', 'POST'], endpoint='edit')
def edit(id):
    ingredient = Ingredient.query.get_or_404(id)
    if request.method == 'POST':
        ingredient.id_ingredient_type = request.form['ingredient_type']
        ingredient.name = request.form['name']
        ingredient.price = request.form['price']
        ingredient.is_vegetarian = request.form.get('is_vegetarian') == 'True'
        ingredient.quantity = request.form['quantity']
        db.session.commit()
        return redirect(url_for('ingredient.index'))
    ingredient_types = IngredientType.query.all()
    return render_template('ingredient/edit.html', ingredient = ingredient, ingredient_types = ingredient_types)

@ingredient_bp.route('/delete/<int:id>', methods=['POST'], endpoint='delete')
def delete(id):
    ingredient = Ingredient.query.get_or_404(id)
    db.session.delete(ingredient)
    db.session.commit()
    return redirect(url_for('ingredient.index'))

@ingredient_bp.route('/supply/<int:id>', methods=['GET'], endpoint='supply')
def supply(id):
    ingredient = Ingredient.query.get_or_404(id)
    if ingredient.id_ingredient_type == 1:
        ingredient.quantity += 5
    elif ingredient.id_ingredient_type == 2:
        ingredient.quantity += 10
    db.session.commit()
    return redirect(url_for('ingredient.index'))

@ingredient_bp.route('/its_healthy/<int:id>', methods=['GET'], endpoint='its_healthy')
def its_healthy(id):
    ingredient = Ingredient.query.get_or_404(id)
    if ingredient.calories < 100 or ingredient.is_vegetarian:
        its_healthy_message = 'El ingrediente es sano'
    else:
        its_healthy_message = 'El ingrediente no es sano'
    return redirect(url_for('ingredient.index', its_healthy=its_healthy_message))
