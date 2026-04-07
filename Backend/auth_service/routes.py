from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt

from models import User, db
from config import Config


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json

    if User.query.filter_by(username=data["username"]).first():
        return {"msg":"User exists"}, 400

    user = User(
        username=data["username"],
        email=data.get("email")
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return {"msg":"Registered successfully"}

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return {"msg":"Invalid credentials"}, 401


    # 🔥 CREATE JWT
    token = jwt.encode({

        "user_id": user.id,
        "username": user.username,

        # Expiry
        "exp": datetime.utcnow() + timedelta(days=Config.JWT_EXPIRE_DAYS)

    }, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)


    return jsonify({"token": token})


def verify_token(token):

    try:
        data = jwt.decode(
            token,
            Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )

        return data   # user info

    except:
        return None
