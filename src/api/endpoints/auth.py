from flask import Blueprint, jsonify, request
from sqlalchemy import select, or_
from api.extensions import jwt, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/token", methods=['POST'])
def create_token():

    body = request.get_json()

    identifier = body.get("identifier", None) 
    
    
    password = body.get("password")

    if not identifier and not password:
        return jsonify({"message": "send credentials to get the token"}),400
    
    if not identifier:
        return jsonify({"message": "send an identifier to get identificated"}),400
    
    user = db.session.execute(select(User).where(or_(User.username == identifier, User.email == identifier), User.is_active == True)).scalars().first()

    if not user:
        return jsonify({"message": "user not found" }),404
    
    if not password:
        return jsonify({"message": "send a password to get identificated"}),400
    

    password_check = user.check_password(password)

    if not password_check:
        return jsonify({"message": "invalid password"}),401

    access_token = create_access_token(identity=user.user)

    return jsonify({"token": access_token, "user_id": user.id, "username": user.username})


@auth_bp.route("/private", methods=['POST'])
@jwt_required()
def private_access():

    current_username= get_jwt_identity()

    user = db.session.execute(select(User).where(User.username == current_username)).scalars().first()

    if not user:
        return jsonify({"message": "invalid token"}),401
    
    return jsonify({"id": user.id, "username" : user.username}),200
    

    