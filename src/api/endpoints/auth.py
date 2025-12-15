from flask import Blueprint, jsonify, request
from sqlalchemy import select, or_, func
from api.extensions import jwt, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.models import Sailor
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/token", methods=['POST'])
def create_token():

    body = request.get_json()

    identificator = body.get("identificator", None) 
    
    password = body.get("password")


    
    if not identificator and not password:
        return jsonify({"message": "send credentials to get the token"}),400
    
    if not identificator:
        return jsonify({"message": "send an identificator to get identificated"}),400
    
    identificator = identificator.replace(" ", "")
    
    sailor = db.session.execute(select(Sailor).where(or_(func.lower(Sailor.sailor_name) == identificator.lower() , func.lower(Sailor.email) == identificator.lower()), Sailor.is_active.is_(True))).scalars().first()


    if not sailor:
        return jsonify({"message": "sailor not found" }),404
    
    if not password:
        return jsonify({"message": "send a password to get identificated"}),400
    
    if not isinstance(password, str):
        password = str(password)
        
    if len(password) < 6:
        return jsonify({"message": "password must be 6 or more characters"}), 400

    password_check = sailor.check_password(password)

    if not password_check:
        return jsonify({"message": "invalid password"}),401

    access_token = create_access_token(identity=sailor.sailor_name, expires_delta=timedelta(minutes=30))

    return jsonify({"token": access_token, "sailor_id": sailor.id, "sailor_name": sailor.sailor_name})


@auth_bp.route("/private", methods=['POST'])
@jwt_required()
def private_access():

    current_sailorname= get_jwt_identity()

    sailor = db.session.execute(select(Sailor).where(Sailor.sailor_name == current_sailorname)).scalars().first()

    if not sailor:
        return jsonify({"message": "invalid token"}),401
    
    return jsonify({"id": sailor.id, "sailor_name" : sailor.sailor_name}),200
    

@jwt.expired_token_loader
def expired_token_callback(jwtheader,jwt_payload):
    return jsonify({"message": "The toke has expire, log in again"}), 401

    