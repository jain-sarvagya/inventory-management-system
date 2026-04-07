from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Order(db.Model):

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)

    total_amount = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(50), default="PENDING")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class OrderItem(db.Model):

    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, nullable=False)

    product_id = db.Column(db.Integer, nullable=False)

    product_name = db.Column(db.String(150), nullable=False)  # ✅ NEW

    quantity = db.Column(db.Integer, nullable=False)

    price = db.Column(db.Float, nullable=False)
