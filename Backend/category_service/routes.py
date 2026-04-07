from flask import Blueprint, request, jsonify
from models import Category, db
from middleware import jwt_required


category_bp = Blueprint("category", __name__)

@category_bp.route("/categories", methods=["POST"])
@jwt_required
def add_category():

    data = request.json

    name = data.get("name")

    if not name:
        return {"msg": "Name required"}, 400


    user_id = request.user["user_id"]

    cat = Category(
        name=name,
        created_by=user_id
    )

    db.session.add(cat)
    db.session.commit()

    return {"msg": "Category added"}

@category_bp.route("/categories", methods=["GET"])
@jwt_required
def get_categories():

    cats = Category.query.all()

    result = []

    for c in cats:
        result.append({
            "id": c.id,
            "name": c.name,
            "created_by": c.created_by
        })

    return jsonify(result)

@category_bp.route("/categories/<int:user_id>", methods=["GET"])
@jwt_required
def get_category_by_id(user_id):

    category = Category.query.get(user_id)

    if not category:
        return {"message": "Category not found"}, 404

    return {
        "id": category.id,
        "name": category.name,
        "created_by": category.created_by
    }, 200

