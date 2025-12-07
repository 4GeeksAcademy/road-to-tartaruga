from flask import Blueprint, jsonify, request
from sqlalchemy import select, or_
from api.extensions import db
from api.models import Sailor

sailors_bp = Blueprint('sailors', __name__, url_prefix="/sailors")





@sailors_bp.route("/", methods=['GET'])
def get_sailors():

    sailor_id = request.args.get("sailor_id")

    if not request.args:

        sailors = list(db.session.execute(select(Sailor)).scalars().all())
        return jsonify({"sailors": [sailor.get_basic_info() for sailor in sailors]}),200
    
    if not sailor_id:
        return jsonify({"message": "send a valid query param"}),400
    

    sailor = db.session.get(Sailor, sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found with provided sailor_id"}), 400

    return jsonify(sailor.serialize()),200





@sailors_bp.route("/", methods=['POST'])
def create_sailor():

    body = request.get_json()
    sailor_name = body.get("sailor_name")
    email = body.get("email")
    password = body.get("password")

    if not sailor_name or not email or not password:
        return jsonify({"message": "email, sailor_name and password are required fields"}), 400

    exist_sailor = db.session.execute(select(Sailor).where(or_(Sailor.sailor_name == sailor_name, Sailor.email == email))).scalars().first()

    if exist_sailor:
        return jsonify({"message": "this sailor_name or email already exist"}),400
    

    
    sailor = Sailor(email=email, sailor_name=sailor_name)

    sailor.set_password(password)

    db.session.add(sailor)
    db.session.commit()    

    return jsonify(sailor.get_basic_info()),200


@sailors_bp.route("/", methods=['PATCH'])
def edit_sailor():

    body = request.get_json()

    if not body:
        return jsonify({
            "message": "you must send info to edit a sailor, for example: email, sailor_name or password"
        })
    
    sailor_id = body.get("sailor_id")
    email = body.get("email")
    sailor_name = body.get("sailor_name")
    password = body.get("password")

    if not sailor_id:
        return jsonify({"message": "we need to recieve an sailor_id to edit it"}),400
    
    sailor = db.session.get(Sailor, sailor_id)

    if not sailor: 
        return jsonify({"message": "sailor not found with provided sailor_id"}), 404

    if not email and not sailor_name and not password:
        return jsonify({"message": "you must send an email, sailorname or password to edit the sailor"}),400
    

    exist_sailor_name = db.session.execute(select(Sailor).where(Sailor.sailor_name == sailor_name, Sailor.id != sailor_id)).scalars().first()
    exist_email = db.session.execute(select(Sailor).where(Sailor.email == email, Sailor.id != sailor_id)).scalars().first()

    if exist_sailor_name and exist_email:
        return jsonify({"message": "already exist an sailor with the provided sailor_name and email"}),400
    
    if exist_sailor_name:
        return jsonify({
            "message": "already exist an sailor with the provided sailor_name"
        }), 400
    if exist_email:
        return jsonify({
                    "message": "already exist an sailor with the provided email"
                }), 400
    
  
    changes= 0

    for key, value in body.items():

        
        if key in ["email", "sailor_name", "password"]:

            if key == "password":
                if not sailor.check_password(value):
                    sailor.set_password(value)
                    changes += 1
            else:
               if getattr(sailor,key) != value:
                setattr(sailor,key, value)
                changes += 1

    if changes == 0:   
        return jsonify({ "message": "you must send different information to edit the sailor" }), 400
    
    print(changes)


    db.session.commit()

    return jsonify(sailor.get_basic_info())
    





# @sailors_bp.route("/", methods=['DELETE'])
# def delete_sailor():

#     if not request.args:
#         return jsonify({"message": "you must use the sailor_id queryparam to delete an sailor"}),400
#     sailor_id = request.args.get("sailor_id")

#     if not sailor_id:
#         return jsonify({"message": "you must send a sailor_id using queryparam"}),400
    
#     sailor = db.session.get(Sailor, sailor_id)

#     if not sailor: 
#         return jsonify({"message": "sailor not found with the provided sailor_id, try another one"}),400
    
#     db.session.delete(sailor)
#     db.session.commit()

#     return jsonify({"done": True}), 200
    