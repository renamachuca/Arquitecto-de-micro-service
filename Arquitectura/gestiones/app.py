from flask import Flask, jsonify, request
from marshmallow import Schema, fields
from gestiones.models import Product
from .database import db, init_db

app = Flask(__name__)
init_db(app)

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()  
    price = fields.Float(required=True)
    stock = fields.Int(required=True) 

@app.route('/')
def home():
    return "¡Aplicación Flask funcionando!"

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    schema = ProductSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_product = Product(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        stock=data['stock']
    )

    db.session.add(new_product)
    db.session.commit()

    return schema.jsonify(new_product), 201

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    schema = ProductSchema(many=True)
    return schema.jsonify(products), 200

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    schema = ProductSchema()
    return schema.jsonify(product), 200

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    schema = ProductSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    product.name = data['name']
    product.description = data.get('description')
    product.price = data['price']
    product.stock = data['stock']

    db.session.commit()

    return schema.jsonify(product), 200

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
