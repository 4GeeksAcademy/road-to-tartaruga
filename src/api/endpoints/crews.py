from flask import Blueprint, jsonify, request
from api.extensions import db
from sqlalchemy import select
import uuid
from api.models import Crew, CrewSailor, Sailor, CrewSailorStatus, Contribution, ClaudeMission


#Genera codigo de invitacion irrepetible
def generate_invite_code():
    return uuid.uuid4().hex


crews_bp = Blueprint("crews", __name__, url_prefix="crews")

@crews_bp.route("/", methods=['GET'])
def get_crews():

    query_params = request.args

    if not query_params:
        crews = list(db.session.execute(select(Crew)).scalars().all())
        return jsonify({"crews": [crew.get_basic_info() for crew in crews]})
    
    crew_id = request.args.get("crew_id")

    if not crew_id:
        return jsonify({"message": "invalid queryparam, please provide a crew_id"}),400
    
    crew = db.session.get(Crew, crew_id)

    if not crew:
        return jsonify({"message": "crew not found"}),404
    
    return jsonify(crew.serialize()),200



@crews_bp.route("/", methods=['POST'])
def create_crew():

    body = request.get_json()

    sailor_id = body.get("sailor_id", None)
    name = body.get("name")
    cm_id = body.get("claude_mission_id", None)

    if not cm_id:
        return jsonify({"message": "claude_mission_id is necessary to add crew contributions"}),400

    claude_mission = db.session.get(ClaudeMission, cm_id)

    if not claude_mission:
        return jsonify({"message": "claude_misssion not found"}), 404

    if not sailor_id and not name:
        return jsonify({
            "message": "sailor_id and name are required fields"
        }),400

    if not sailor_id:
        return jsonify({
            "message": "please provide an sailor_id to create the crew"
        }), 400
    
    sailor = db.session.get(Sailor, sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found with the provided sailor_id"}), 404
    
    if not name:
        return jsonify({
            "message": "please provide a name to create a crew"
        }),400
    
    exist_crew = db.session.execute(select(Crew).where(Crew.name==name)).scalars().first()

    if exist_crew:
        return jsonify({
            "message": "already exist this crew name, try another one"
        }),400
    
    sailor_crews = db.session.execute(select(CrewSailor).where(CrewSailor.sailor_id == sailor_id)).scalars().all()

    sailor_quantity_crews = len(sailor_crews)

    print([sailor_crew.crew.name for  sailor_crew in sailor_crews])

    if sailor_quantity_crews >= 3:
        return jsonify({"message": "sailor crews limit has been reached 3 of 3"}),400
    
    created_crews = db.session.execute(select(Crew).where(Crew.creator_id == sailor_id)).scalars().all()

    created_crews_quantity = len(created_crews)

    if created_crews_quantity >= 2:
        return jsonify({"message": "sailor crews created limit has been reached 2 of 2"}),404

    crew = Crew(name=name, creator_id=sailor_id, creator_name=sailor.sailor_name)

    db.session.add(crew)
    db.session.commit()

    contributions = Contribution(crew_id= crew.id, claude_mission_id=cm_id, is_crew=True) 

    db.session.add(contributions)
    db.session.commit()

    crew_id = crew.id
    crew_user = CrewSailor(sailor_id=sailor_id, crew_id=crew_id, is_captain=True, status=CrewSailorStatus.ACTIVE)
    db.session.add(crew_user)
    db.session.commit()


    return jsonify(crew.get_basic_info()), 200








@crews_bp.route("/", methods=['PATCH'])
def edit_crew():

    body = request.get_json()

    sailor_id = body.get("sailor_id", None)
    crew_id = body.get("crew_id", None)
    name = body.get("name", None)

    if not sailor_id and not crew_id and not name:
        return jsonify({"message": "sailor_id , crew_id and name are required fields"}),400

    if not sailor_id:
        return jsonify({"message": "sailor_id are required"}),400
    
    if not crew_id:
        return jsonify({"message": "crew_id are required"}),400
    
    if not name:
        return jsonify({"message": "name are required"}),400
    
    sailor = db.session.get(Sailor, sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found with the provided sailor_id"}), 404
    
    crew = db.session.get(Crew, crew_id)

    if not crew:
        return jsonify({"message": "crew not found with the provided crew_id"}), 404
    
    crew_sailor = db.session.execute(select(CrewSailor).where(CrewSailor.sailor_id == sailor_id, CrewSailor.crew_id == crew_id)).scalars().first()

    if not crew_sailor:
        return jsonify({"message": "this sailor is not a member of the crew"}),404
    
    if not crew_sailor.is_captain:
        return jsonify({"message": "you need to be captain to modify the crew information"}), 401
    
    exist_name = db.session.execute(select(Crew).where(Crew.name == name)).scalars().first()

    if exist_name:
        return jsonify({"message": "already exist a crew with this name"}), 400
    
    crew.name = name
    db.session.commit()

    return jsonify(crew.get_basic_info())






@crews_bp.route("/", methods=['DELETE'])
def delete_crew():

    body = request.get_json()

    sailor_id = body.get("sailor_id", None)
    crew_id = body.get("crew_id", None)

    if not sailor_id and not crew_id:
        return jsonify({"message": "sailor_id, crew_id and name are required fields"}),400

    if not sailor_id:
        return jsonify({"message": "sailor_id are required"}),400
    
    if not crew_id:
        return jsonify({"message": "crew_id are required"}),400
    
    sailor = db.session.get(Sailor, sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found with the provided sailor_id"}), 404
    
    crew = db.session.get(Crew, crew_id)

    if not crew:
        return jsonify({"message": "crew not found with the provided crew_id"}), 404

    crew_sailor = db.session.execute(select(CrewSailor).where(CrewSailor.sailor_id == sailor_id, CrewSailor.crew_id == crew_id)).scalars().first()

    if not crew_sailor:
        return jsonify({"message": "this sailor is not a member of the crew"}),404
    
    if not crew_sailor.is_captain:
        return jsonify({"message": "you need to be captain to delete the crew"}), 401
    

    db.session.delete(crew)
    db.session.commit()

    return jsonify({"done": True}),200