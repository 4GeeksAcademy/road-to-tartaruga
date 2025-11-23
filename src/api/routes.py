"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.endpoints.users import users_bp
from api.endpoints.crews import crews_bp
from api.endpoints.missions import missions_bp
api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

api.register_blueprint(users_bp)
api.register_blueprint(crews_bp)
api.register_blueprint(missions_bp)



@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200
