from db import db

class IngredientType(db.Model):

    __tablename__ = 'ingredient_type'
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(50), nullable = True)

    def __init__(self, type: str) -> None:
        self.type = type

    