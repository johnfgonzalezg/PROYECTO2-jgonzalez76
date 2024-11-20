from db import db

class Product(db.Model):

    __tablename = 'product'
    id = db.Column(db.Integer, primary_key = True)
    id_product_type = db.Column(db.Integer, db.ForeignKey('product_type.id'), nullable = False)
    name = db.Column(db.String(200), nullable = False)
    calories = db.Column(db.Integer, nullable = False)
    cost = db.Column(db.Numeric(10, 2), nullable = False)
    public_price = db.Column(db.Numeric(10, 2), nullable = False)
    profitability = db.Column(db.Numeric(10, 2), nullable = False)
    cup_type = db.Column(db.String(100))

    def __init__(self, id_product_type: int, name: str, public_price: float, cup_type: str = None) -> None:
        self.id_product_type = id_product_type
        self.name = name
        self.public_price = public_price
        self.calories = 0
        self.cost = 0
        self.profitability = 0
        self.cup_type = cup_type if cup_type != None else ''

    #Getters y Setters
    def get_id_product_type(self) -> int:
        return self.id_product_type
    
    def set_id_product_type(self, id_product_type: int) -> None:
        if isinstance(id_product_type, int):
            self.id_product_type = id_product_type
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
    
    def get_cost(self) -> float:
        return self.cost
    
    def set_cost(self, cost: float) -> None:
        if isinstance(cost, float):
            self.cost = cost
        else:
            raise ValueError('El valor debe ser un flotante.')
    
    def get_public_price(self) -> float:
        return self.public_price
    
    def set_public_price(self, public_price: float) -> None:
        if isinstance(public_price, float):
            self.public_price = public_price
        else:
            raise ValueError('El valor debe ser un flotante.')
    
    def get_profitability(self) -> float:
        return self.profitability
    
    def set_profitability(self, profitability: float) -> None:
        if isinstance(profitability, float):
            self.profitability = profitability
        else:
            raise ValueError('El valor debe ser un flotante.')
