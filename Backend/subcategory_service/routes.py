from flask import Blueprint, request, jsonify
from models import SubCategory, db
from middleware import jwt_required


subcat_bp = Blueprint("subcategory", __name__)

@subcat_bp.route("/subcategories", methods=["POST"])
@jwt_required
def add_subcategory():

    data = request.json

    name = data.get("name")
    category_id = data.get("category_id")

    if not name or not category_id:
        return {"msg": "Name & category_id required"}, 400


    user_id = request.user["user_id"]

    sub = SubCategory(
        name=name,
        category_id=category_id,
        created_by=user_id
    )

    db.session.add(sub)
    db.session.commit()

    return {"msg": "Subcategory added"}

@subcat_bp.route("/subcategories", methods=["GET"])
@jwt_required
def get_subcategories():

    subs = SubCategory.query.all()

    result = []

    for s in subs:
        result.append({
            "id": s.id,
            "name": s.name,
            "category_id": s.category_id,
            "created_by": s.created_by
        })

    return jsonify(result)

@subcat_bp.route("/categories/<int:cid>/subcategories")
@jwt_required
def by_category(cid):

    subs = SubCategory.query.filter_by(category_id=cid).all()

    return jsonify([
        {
            "id": s.id,
            "name": s.name
        } for s in subs
    ])
