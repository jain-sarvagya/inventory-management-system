from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False)

    created_by = db.Column(db.Integer)  # user_id
