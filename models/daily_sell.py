from db import db
from datetime import datetime

class DailySells(db.Model):

    __tablename__ = 'daily_sell'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    sell_date = db.Column(db.Date, nullable = False)
    total_sell_value = db.Column(db.Numeric(10, 2), nullable = False)

    def __init__(self, sell_date: datetime, total_sell_value: float) -> None:
       self.sell_date = sell_date
       self.total_sell_value = total_sell_value
    
    # Getters and Setters

    def get_sell_date(self) -> datetime:
        return self.sell_date
    
    def set_sell_date(self, sell_date) -> None:
        if isinstance(sell_date, datetime):
            self.sell_date = sell_date
        else:
            raise ValueError('El valor debe ser de tipo datetime.')
        
    def get_total_sell_value(self) -> float:
        return self.total_sell_value
    
    def set_total_sell_value(self, total_sell_value: float) -> None:
        if isinstance(total_sell_value, float):
            self.total_sell_value += total_sell_value
        else:
            raise ValueError('El valor debe ser de tipo flotante.')