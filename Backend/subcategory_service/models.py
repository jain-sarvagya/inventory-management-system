from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SubCategory(db.Model):

    __tablename__ = "subcategories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    category_id = db.Column(db.Integer, nullable=False)

    created_by = db.Column(db.Integer)
