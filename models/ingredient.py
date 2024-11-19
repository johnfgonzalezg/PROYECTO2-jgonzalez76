from db import db

class Ingredient(db.Model):

    __tablename = 'ingredient'
    id = db.Column(db.Integer, primary_key = True)
    id_ingredient_type = db.Column(db.Integer, db.ForeignKey('ingredient_type.id'), nullable = False)
    name = db.Column(db.String(200), nullable = False)
    calories = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Numeric(10, 2), nullable = False)
    is_vegetarian = db.Column(db.Boolean)
    quantity = db.Column(db.Numeric(10,2), nullable = False)
    flavor = db.Column(db.String(50))
    
    def __init__(self, id_ingredient_type: int, name: str, calories: int, price: float, is_vegetarian: bool, quantity: int, flavor: str = None) -> None:
        self.id_ingredient_type = id_ingredient_type
        self.name = name
        self.calories = calories
        self.price = price
        self.is_vegetarian = is_vegetarian
        self.quantity = quantity
        self.flavor = flavor if flavor != None else ''

    #Getters y Setters
    def get_id_ingredient_type(self) -> int:
        return self.id_ingredient_type
    
    def set_id_ingredient_type(self, id_ingredient_type: int) -> None:
        if isinstance(id_ingredient_type, int):
            self.id_ingredient_type = id_ingredient_type
        else:
            raise ValueError('El valor debe ser un entero.')
        
    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        if isinstance(name, str):
            self.name = name
        else:
            raise ValueError('El valor debe ser un string.')
    
    def get_calories(self) -> int:
        return self.calories
    
    def set_calories(self, calories: int) -> None:
        if isinstance(calories, int):
            self.calories = calories
        else:
            raise ValueError('El valor debe ser un entero.')
    
    def get_price(self) -> float:
        return self.price
    
    def set_price(self, price: float) -> None:
        if isinstance(price, float):
            self.price = price
        else:
            raise ValueError('El valor debe ser un float.')
    
    def get_is_vegetarian(self) -> bool:
        return self.is_vegetarian
    
    def set_is_vegetarian(self, is_vegetarian: bool) -> None:
        if isinstance(is_vegetarian, bool):
            self.is_vegetarian = is_vegetarian
        else:
            raise ValueError('El valor debe ser un booleano.')
    
    def get_quantity(self) -> int:
        return self.quantity
    
    def set_quantity(self, quantity: int) -> None:
        if isinstance(quantity, int):
            self.quantity = quantity
        else:
            raise ValueError('El valor debe ser un entero.')
        
    def get_flavor(self) -> str:
        return self.flavor
    
    def set_flavor(self, flavor: str) -> None:
        if isinstance(flavor, str):
            self.flavor = flavor
        else:
            raise ValueError('El valor debe ser un string.')