from flask import request, jsonify
from functools import wraps
import jwt
from config import Config


def jwt_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"msg": "Token missing"}), 401


        try:
            # Format: Bearer TOKEN
            token = auth_header.split(" ")[1]

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
