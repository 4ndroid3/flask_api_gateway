from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests

app = Flask(__name__)

# Configuración JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# Configuración del rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Aquí deberías validar el usuario y la contraseña
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Ruta protegida con JWT y limitada por el rate limiter
@app.route('/protected', methods=['GET'])
@jwt_required()
@limiter.limit("5 per minute")
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# Ruta para hacer una solicitud HTTP externa
@app.route('/protected_book', methods=['GET'])
@jwt_required()
def protected_book():
    headers = {'Authorization': 'Bearer YLMHXNLg0rLVeMN_5exS'}
    response = requests.get('https://the-one-api.dev/v2/book', headers=headers, timeout=10)
    return jsonify(response.json()), response.status_code


@app.route('/protected_movie', methods=['GET'])
@jwt_required()
def protected_movie():
    headers = {'Authorization': 'Bearer YLMHXNLg0rLVeMN_5exS'}
    response = requests.get('https://the-one-api.dev/v2/book', headers=headers, timeout=10)
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    app.run()
