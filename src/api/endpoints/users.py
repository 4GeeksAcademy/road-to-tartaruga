from flask import Blueprint, jsonify, request
from sqlalchemy import select, or_
from api.models import User
from api.extensions import db


users_bp = Blueprint('users', __name__, url_prefix="/users")





# @users_bp.route("/", methods=['GET'])
# def get_users():

#     user_id = request.args.get("user_id")

#     if not request.args:

#         users = list(db.session.execute(select(User)).scalars().all())
#         return jsonify({"users": [user.serialize() for user in users]}),200
    
#     if not user_id:
#         return jsonify({"message": "send a valid query param"}),400
    

#     user = db.session.get(User, user_id)

#     if not user:
#         return jsonify({"message": "user not found with provided user_id"}), 400

#     return jsonify(user.get_info()),200




# @users_bp.route("/", methods=['POST'])
# def create_user():

#     body = request.get_json()
#     username = body.get("username")
#     email = body.get("email")
#     password = body.get("password")

#     user = db.session.execute(select(User).where(or_(User.username == username, User.email == email))).scalars().first()

#     if user:
#         return jsonify({"message": "this username or email already exist"}),400
    
#     user = User(email=email, username=username)

#     user.set_password(password)

#     db.session.add(user)
#     db.session.commit()    

#     return jsonify(user.get_info()),200


# @users_bp.route("/", methods=['PATCH'])
# def edit_user():

#     body = request.get_json()

#     if not body:
#         return jsonify({
#             "message": "you must send info to edit a user, for example: email, username or password"
#         })
    
#     user_id = body.get("user_id")
#     email = body.get("email")
#     username = body.get("username")
#     password = body.get("password")

#     if not user_id:
#         return jsonify({"message": "we need to recieve an user_id to edit it"}),400
    
#     user = db.session.get(User, user_id)

#     if not user: 
#         return jsonify({"message": "user not found with provided user_id"}), 404

#     if not email and not username and not password:
#         return jsonify({"message": "you must send an email, username or password to edit the user"}),400
    

#     exist_username = db.session.execute(select(User).where(User.username == username, User.id != user_id)).scalars().first()
#     exist_email = db.session.execute(select(User).where(User.email == email, User.id != user_id)).scalars().first()

#     if exist_username and exist_email:
#         return jsonify({"message": "already exist an user with the provided username and email"}),400
    
#     if exist_username:
#         return jsonify({
#             "message": "already exist an user with the provided username"
#         }), 400
#     if exist_email:
#         return jsonify({
#                     "message": "already exist an user with the provided email"
#                 }), 400
    
  
#     changes= 0

#     for key, value in body.items():

        
#         if key in ["email", "username", "password"]:

#             if key == "password":
#                 if not user.check_password(value):
#                     user.set_password(value)
#                     changes += 1
#             else:
#                if getattr(user,key) != value:
#                 setattr(user,key, value)
#                 changes += 1

#     if changes == 0:   
#         return jsonify({ "message": "you must send different information to edit the user" }), 400
    
#     print(changes)


#     db.session.commit()

#     return jsonify(user.get_info())
    





# @users_bp.route("/", methods=['DELETE'])
# def delete_user():

#     if not request.args:
#         return jsonify({"message": "you must use the user_id queryparam to delete an user"}),400
#     user_id = request.args.get("user_id")

#     if not user_id:
#         return jsonify({"message": "you must send a user_id using queryparam"}),400
    
#     user = db.session.get(User, user_id)

#     if not user: 
#         return jsonify({"message": "user not found with the provided user_id, try another one"}),400
    
#     db.session.delete(user)
#     db.session.commit()

#     return jsonify({"done": True}), 200
    