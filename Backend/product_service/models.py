from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    category_id = db.Column(db.Integer, nullable=False)

    subcategory_id = db.Column(db.Integer, nullable=False)

    price = db.Column(db.Float, nullable=False)

    stock = db.Column(db.Integer, default=0)

    description = db.Column(db.Text)

    created_by = db.Column(db.Integer)
