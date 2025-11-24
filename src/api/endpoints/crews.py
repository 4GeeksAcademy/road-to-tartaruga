from flask import Blueprint, jsonify, request
from api.models import Crew, CrewUser, User
from api.extensions import db
from sqlalchemy import select
import uuid


#Genera codigo de invitacion irrepetible
def generate_invite_code():
    return uuid.uuid4().hex


crews_bp = Blueprint("crews", __name__, url_prefix="crews")

@crews_bp.route("/", methods=['GET'])
def get_crews():

    query_params = request.args

    if not query_params:
        crews = list(db.session.execute(select(Crew)).scalars().all())
        return jsonify({"crews": [crew.serialize() for crew in crews]})
    
    crew_id = request.args.get("crew_id")

    if not crew_id:
        return jsonify({"message": "invalid queryparam, please provide a crew_id"}),400
    
    crew = db.session.get(Crew, crew_id)

    if not crew:
        return jsonify({"message": "crew not found"}),404
    
    return jsonify(crew.get_info())



@crews_bp.route("/", methods=['POST'])
def create_crew():

    body = request.get_json()

    user_id = body.get("user_id", None)
    name = body.get("name")

    if not user_id and not name:
        return jsonify({
            "message": "user_id and name are required fields"
        }),400

    if not user_id:
        return jsonify({
            "message": "please provide an user_id to create the crew"
        }), 400
    
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"message": "user not found with the provided user_id"}), 404
    
    if not name:
        return jsonify({
            "message": "please provide a name to create a crew"
        }),400
    
    exist_crew = db.session.execute(select(Crew).where(Crew.name==name)).scalars().first()

    if exist_crew:
        return jsonify({
            "message": "already exist this crew name, try another one"
        }),400
    
    user_crews = db.session.execute(select(CrewUser).where(CrewUser.user_id == user_id)).scalars().all()

    user_quantity_crews = len(user_crews)

    if user_quantity_crews >= 3:
        return jsonify({"message": "user crews limit has been reached 3 of 3"}),400

    crew = Crew(name=name)

    db.session.add(crew)
    db.session.commit()

    crew_id = crew.id
    crew_user = CrewUser(user_id=user_id, crew_id=crew_id, is_admin=True)
    db.session.add(crew_user)
    db.session.commit()


    return jsonify(crew.get_info()), 200



@crews_bp.route("/", methods=['PATCH'])
def edit_crew():

    body = request.get_json()

    user_id = body.get("user_id", None)
    crew_id = body.get("crew_id", None)
    name = body.get("name", None)

    if not user_id and not crew_id and not name:
        return jsonify({"message": "user_id, crew_id and name are required fields"}),400

    if not user_id:
        return jsonify({"message": "user_id are required"}),400
    
    if not crew_id:
        return jsonify({"message": "crew_id are required"}),400
    
    if not name:
        return jsonify({"message": "name are required"}),400
    
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"message": "user not found with the provided user_id"}), 404
    
    crew = db.session.get(Crew, crew_id)

    if not crew:
        return jsonify({"message": "crew not found with the provided crew_id"}), 404
    
    crew_user = db.session.execute(select(CrewUser).where(CrewUser.user_id == user_id, CrewUser.crew_id == crew_id)).scalars().first()

    if not crew_user:
        return jsonify({"message": "this user is not a member of the crew"}),404
    
    if not crew_user.is_admin:
        return jsonify({"message": "you need to be admin to modify the crew information"}), 401
    
    exist_name = db.session.execute(select(Crew).where(Crew.name == name)).scalars().first()

    if exist_name:
        return jsonify({"message": "already exist a crew with this name"}), 400
    
    crew.name = name
    db.session.commit()

    return jsonify(crew.get_info())


@crews_bp.route("/", methods=['DELETE'])
def delete_crew():

    body = request.get_json()

    user_id = body.get("user_id", None)
    crew_id = body.get("crew_id", None)

    if not user_id and not crew_id:
        return jsonify({"message": "user_id, crew_id and name are required fields"}),400

    if not user_id:
        return jsonify({"message": "user_id are required"}),400
    
    if not crew_id:
        return jsonify({"message": "crew_id are required"}),400
    
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"message": "user not found with the provided user_id"}), 404
    
    crew = db.session.get(Crew, crew_id)

    if not crew:
        return jsonify({"message": "crew not found with the provided crew_id"}), 404

    crew_user = db.session.execute(select(CrewUser).where(CrewUser.user_id == user_id, CrewUser.crew_id == crew_id)).scalars().first()

    if not crew_user:
        return jsonify({"message": "this user is not a member of the crew"}),404
    
    if not crew_user.is_admin:
        return jsonify({"message": "you need to be admin to delete the crew"}), 401
    

    db.session.delete(crew)
    db.session.commit()

    return jsonify({"done": True}),200