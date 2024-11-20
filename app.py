from flask import Flask, render_template
from db import db, init_db
from dotenv import load_dotenv
from controllers.init_values import insert_initial_values
from models.ingredient import Ingredient
from models.product import Product
import os
from controllers.ice_cream_shop_controller import ice_cream_shop_bp
from controllers.product_controller import product_bp
from controllers.ingredient_controller import ingredient_bp

load_dotenv()

app = Flask(__name__, template_folder = 'views')

app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_db(app)
insert_initial_values(app)

# Importa y registra los blueprints de los controladores
app.register_blueprint(ice_cream_shop_bp, url_prefix='/')
app.register_blueprint(product_bp, url_prefix='/product')
app.register_blueprint(ingredient_bp, url_prefix='/ingredient')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)