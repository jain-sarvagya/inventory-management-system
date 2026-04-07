from flask import Blueprint, request, jsonify
from models import Product, db
from middleware import jwt_required


product_bp = Blueprint("product", __name__)

@product_bp.route("/products", methods=["POST"])
@jwt_required
def add_product():

    data = request.json

    name = data.get("name")
    cat_id = data.get("category_id")
    sub_id = data.get("subcategory_id")
    price = data.get("price")
    stock = data.get("stock", 0)
    desc = data.get("description")


    if not all([name, cat_id, sub_id, price]):
        return {"msg": "Missing required fields"}, 400


    user_id = request.user["user_id"]

    prod = Product(
        name=name,
        category_id=cat_id,
        subcategory_id=sub_id,
        price=price,
        stock=stock,
        description=desc,
        created_by=user_id
    )

    db.session.add(prod)
    db.session.commit()

    return {"msg": "Product added"}

@product_bp.route("/products", methods=["GET"])
@jwt_required
def get_products():

    products = Product.query.all()

    result = []

    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock,
            "category_id": p.category_id,
            "subcategory_id": p.subcategory_id
        })

    return jsonify(result)

@product_bp.route("/products/<int:pid>")
@jwt_required
def get_product(pid):

    p = Product.query.get_or_404(pid)

    return jsonify({
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "stock": p.stock,
        "description": p.description
    })

@product_bp.route("/products/<int:pid>", methods=["PUT"])
@jwt_required
def update_product(pid):

    p = Product.query.get_or_404(pid)

    data = request.json

    p.name = data.get("name", p.name)
    p.price = data.get("price", p.price)
    p.stock = data.get("stock", p.stock)
    p.description = data.get("description", p.description)

    db.session.commit()

    return {"msg": "Updated"}


@product_bp.route("/products/<int:pid>", methods=["DELETE"])
@jwt_required
def delete_product(pid):

    p = Product.query.get_or_404(pid)

    db.session.delete(p)
    db.session.commit()

    return {"msg": "Deleted"}

@product_bp.route("/products/<int:pid>/info", methods=["GET"])
@jwt_required
def product_info(pid):

    product = Product.query.get_or_404(pid)

    return {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }

@product_bp.route("/products/<int:pid>/reduce", methods=["PUT"])
@jwt_required
def reduce_stock(pid):

    data = request.json

    qty = data.get("quantity")

    product = Product.query.get_or_404(pid)

    if product.stock < qty:
        return {"msg": "Not enough stock"}, 400


    product.stock -= qty

    db.session.commit()

    return {
        "msg": "Stock reduced",
        "new_stock": product.stock
    }
