from flask import Blueprint, jsonify, request
from sqlalchemy import select, or_
from api.extensions import jwt, db
from api.models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/", methods=['POST'])
def create_token():

    body = request.get_json()

    identifier = body.get("username", body.get("email", None)) 
    
    
    password = body.get("password")

    if not identifier and not password:
        return jsonify({"message": "send credentials to get the token"}),400
    
    if not identifier:
        return jsonify({"message": "send an username or email to get identificated"}),400
    
    user = db.session.execute(select(User).where(or_(User.username == identifier, User.email == identifier), User.is_active == True)).scalars().first()

    if not user:
        return jsonify({"message": "user not found" })
    
    if not password:
        return jsonify({"message": "send a password to get identificated"}),400
    

    password_check = user.check_password(password)

    if not password_check:
        return jsonify({"message": "invalid credentials"}),400

    access_token = create_access_token(identity=user.id)

    return jsonify({"token": access_token, "user_id": user.id, "username": user.username})
    