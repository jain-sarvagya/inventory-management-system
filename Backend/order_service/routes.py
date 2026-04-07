from flask import Blueprint, request, jsonify
from models import Order, OrderItem, db
from middleware import jwt_required
import requests
PRODUCT_SERVICE_URL = "http://localhost:5003"



order_bp = Blueprint("order", __name__)

@order_bp.route("/orders", methods=["POST"])
@jwt_required
def create_order():

    data = request.json

    items = data.get("items")

    if not items:
        return {"msg": "Items required"}, 400


    user_id = request.user["user_id"]

    headers = {
        "Authorization": request.headers.get("Authorization")
    }

    total = 0
    order_items_data = []


    # 🔍 Step 1: Get product info + check stock
    for i in items:

        pid = i["product_id"]
        qty = i["quantity"]

        # Call product service
        res = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{pid}/info",
            headers=headers
        )

        if res.status_code != 200:
            return {"msg": f"Product {pid} not found"}, 404


        prod = res.json()

        if prod["stock"] < qty:
            return {
                "msg": f"Not enough stock for {prod['name']}"
            }, 400


        price = prod["price"]
        name = prod["name"]

        total += price * qty


        order_items_data.append({
            "product_id": pid,
            "name": name,
            "price": price,
            "qty": qty
        })


    # 📝 Step 2: Create Order
    order = Order(
        user_id=user_id,
        total_amount=total
    )

    db.session.add(order)
    db.session.flush()


    # 📦 Step 3: Reduce Stock + Save Items
    for item in order_items_data:

        # Reduce stock
        res = requests.put(
            f"{PRODUCT_SERVICE_URL}/products/{item['product_id']}/reduce",
            json={"quantity": item["qty"]},
            headers=headers
        )

        if res.status_code != 200:
            db.session.rollback()

            return {
                "msg": "Stock update failed",
                "error": res.json()
            }, 400


        # Save order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            product_name=item["name"],
            quantity=item["qty"],
            price=item["price"]
        )

        db.session.add(order_item)


    db.session.commit()


    return {
        "msg": "Order placed successfully",
        "order_id": order.id,
        "total": total
    }

@order_bp.route("/orders", methods=["GET"])
@jwt_required
def get_orders():

    orders = Order.query.all()

    result = []

    for o in orders:
        result.append({
            "id": o.id,
            "user_id": o.user_id,
            "total": o.total_amount,
            "status": o.status,
            "date": o.created_at
        })

    return jsonify(result)

@order_bp.route("/my-orders")
@jwt_required
def my_orders():

    user_id = request.user["user_id"]

    orders = Order.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": o.id,
            "total": o.total_amount,
            "status": o.status
        } for o in orders
    ])

@order_bp.route("/orders/<int:oid>/status", methods=["PUT"])
@jwt_required
def update_status(oid):

    order = Order.query.get_or_404(oid)

    status = request.json.get("status")

    order.status = status

    db.session.commit()

    return {"msg": "Status updated"}
