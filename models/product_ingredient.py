from db import db

class ProductIngredient(db.Model):
    
    __tablename__ = 'product_ingredient'
    id = db.Column(db.Integer, primary_key = True)
    id_product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    id_ingredient = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable = False)
    
    def __init__(self, id_product: int, id_ingredient: int) -> None:
        self.id_product = id_product
        self.id_ingredient = id_ingredient
    
