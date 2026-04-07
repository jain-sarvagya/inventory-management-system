from flask import request, jsonify
from functools import wraps
import jwt
from config import Config


def jwt_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        auth = request.headers.get("Authorization")

        if not auth:
            return jsonify({"msg": "Token missing"}), 401


        try:
            # Bearer TOKEN
            token = auth.split(" ")[1]

            data = jwt.decode(
                token,
                Config.JWT_SECRET,
                algorithms=[Config.JWT_ALGORITHM]
            )

            # Save user info
            request.user = data

        except:
            return jsonify({"msg": "Invalid / Expired Token"}), 401


        return f(*args, **kwargs)

    return wrapper
