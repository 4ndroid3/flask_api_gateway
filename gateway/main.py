from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
from gateway.config import limiter

main_bp = Blueprint("main", __name__)


@main_bp.route("/protected", methods=["GET"])
@jwt_required()
@limiter.limit("5 per minute")
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@main_bp.route("/protected_book", methods=["GET"])
@jwt_required()
def protected_book():
    headers = {"Authorization": "Bearer YLMHXNLg0rLVeMN_5exS"}
    response = requests.get(
        "https://the-one-api.dev/v2/book", headers=headers, timeout=10
    )
    return jsonify(response.json()), response.status_code


@main_bp.route("/protected_movie", methods=["GET"])
@jwt_required()
def protected_movie():
    headers = {"Authorization": "Bearer YLMHXNLg0rLVeMN_5exS"}
    response = requests.get(
        "https://the-one-api.dev/v2/movie", headers=headers, timeout=10
    )
    return jsonify(response.json()), response.status_code
