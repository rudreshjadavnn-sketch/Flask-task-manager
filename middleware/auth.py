from flask import request, jsonify
from config import Config
import jwt


def verify_token():

    token = request.headers.get("Authorization")

    if not token:
        return None, jsonify({
            "message": "Unauthorized"
        }), 401

    try:

        decoded = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=["HS256"]
        )

        return decoded, None, None

    except jwt.ExpiredSignatureError:

        return None, jsonify({
            "message": "Token Expired"
        }), 401

    except jwt.InvalidTokenError:

        return None, jsonify({
            "message": "Invalid Token"
        }), 401