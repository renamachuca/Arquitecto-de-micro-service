from .database import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))  
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
