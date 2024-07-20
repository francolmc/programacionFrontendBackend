from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from application.extensions import db
from application.products.models import Products

products_blueprint = Blueprint("products", __name__, url_prefix="/api")

@products_blueprint.route("/products", methods=["GET"])
@cross_origin()
def get_products():
    products = Products.query.all()
    return jsonify([{ "id": product.id, 'product_name': product.prpduct_name, 'price': product.price, 'stock': product.stock } for product in products])

@products_blueprint.route("/products/<int:product_id>", methods=["GET"])
@cross_origin()
def get_product_by_id(product_id):
    product = Products.query.get_or_404(product_id)
    return jsonify({
        "id": product.id,
        "product_name": product.product_name,
        "price": product.price,
        "stock": product.stock
    })

@products_blueprint.route("/products/search", methods=["GET"])
@cross_origin()
def search_products():
    search_text = request.args.get("q")
    if not search_text:
        return jsonify({"message": "Debes proporcionar un texto de búsqueda"}), 400

    products = Products.query.filter(
        (Products.product_name.ilike(f"%{search_text}%"))
    ).all()

    if not products:
        return jsonify({"message": "No products matched the search were found"}), 404

    product_data = [
        {
            "id": product.id,
            "product_name": product.product_name,
            "price": product.price,
            "stock": product.stock,
        }
        for product in products
    ]
    return jsonify(product_data)


@products_blueprint.route("/products", methods=["POST"])
@cross_origin()
def create_product():
    data = request.get_json()
    new_product = Products(
    product_name=data["product_name"],
    price=data["price"],
    stock=data["stock"])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({
        "message": "Product created successfully"
    }), 201

@products_blueprint.route("/products/<int:product_id>", methods=["PUT"])
@cross_origin()
def update_product(product_id):
    product = Products.query.get_or_404(product_id)
    data = request.get_json()
    product.product_name = data.get("product_name", product.product_name)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)
    db.session.commit()
    return jsonify({
        "message": "Product updated successfully"
    })

@products_blueprint.route("/products/<int:product_id>", methods=["DELETE"])
@cross_origin()
def delete_product(product_id):
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({
        "message": "Product deleted successfully"
    })