from db import db

class ProductType(db.Model):

    __tablename__ = 'product_type'
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(50), nullable = True)


    