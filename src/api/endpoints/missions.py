from flask import Blueprint, jsonify, request
from api.models import Mission, db, Sailor, Crew, Objective, CrewSailor
from sqlalchemy import select, func, or_


missions_bp = Blueprint("missions", __name__, url_prefix="missions")

@missions_bp.route("/sailor/<int:sailor_id>", methods=['GET'])
def get_sailor_missions(sailor_id):

    sailor = db.session.get(Sailor, sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found"}), 404
    
    return jsonify(sailor.get_missions_by_state()),200




@missions_bp.route("/crew/<int:crew_id>", methods=['GET'])
def get_crew_missions(crew_id):
    crew = db.session.get(Crew,crew_id)

    if not crew:
        return jsonify({"message": "crew not found"}), 404
    
    return jsonify(crew.get_missions_by_state()),200




@missions_bp.route("/sailor/<int:sailor_id>", methods=['POST'])
def create_sailor_missions(sailor_id):

    sailor = db.session.get(Sailor, sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found"}), 404

    body = request.get_json()

    title = body.get("title")
    description = body.get("title")
    objectives = body.get("objectives")

    for key in ["title", "description", "objectives"]:
        if key not in body:
            return jsonify({"message": f"{key} is a required field"}), 400
        
    existing_mission = db.session.execute(select(Mission).where(or_(
        func.replace(Mission.title, " ", "") == title.replace(" ", ""), 
        func.replace(Mission.description, " ", "") == description.replace(" ", "")
                )
            )
        ).scalars().first()


    if existing_mission:
        return jsonify({"message": "this title or description already exist try another one"}), 400

    if not isinstance(objectives, list):
        return jsonify({"message": "objectives must be a list"}), 400
    
    sailor_missions = db.session.execute(select(Mission).where(Mission.sailor_owner_id == sailor_id, Mission.completed_at.is_(None) )).scalars().all()

    if len(sailor_missions) >= 3:
        return jsonify({"message": "sailor active missions limit has been reached 3 of 3"}), 400
    
    if len(objectives) >3:
        return jsonify({"message": "mission objectives must be a maximum of 3"}),400
    
    if len(objectives) < 2:
        return jsonify({"message": f"objectives must be at least 2, {len(objectives)} recieved"}),400
    
    new_mission = Mission(title=title, description=description, creator_id=sailor_id, sailor_owner_id=sailor_id)
    db.session.add(new_mission)
    db.session.commit()



    for objective in objectives:
        new_objective = Objective(title=objective, assigned_to_id=sailor_id, mission_id =new_mission.id )
        db.session.add(new_objective)
        db.session.commit()
    

    
    return jsonify({"mission": new_mission.get_basic_info(), "objectives": new_mission.get_objectives() }),200







@missions_bp.route("/crew/<int:crew_id>/<int:captain_id>", methods=['POST'])
def create_crew_missions(crew_id, captain_id):

    crew = db.session.get(Crew, crew_id)

    if not crew:
        return jsonify({"message": "crew not found"}), 404
    
    captain = db.session.get(Sailor, captain_id)

    if not captain:
        return jsonify({"message": "sailor not founded"}), 404
    
    crew_sailor = db.session.execute(select(CrewSailor).where(CrewSailor.sailor_id == captain_id, CrewSailor.crew_id == crew_id)).scalars().first()

    if not crew_sailor:
        return jsonify({"message": "this sailor is not part of this crew"}), 404
    
    if not crew_sailor:
        return jsonify({"message": "must be a captain to create a mission on this crew"}), 400


    body = request.get_json()

    title = body.get("title")
    description = body.get("title")
    objectives = body.get("objectives")

    for key in ["title", "description", "objectives"]:
        if key not in body:
            return jsonify({"message": f"{key} is a required field"}), 400
        
    existing_mission = db.session.execute(select(Mission).where(or_(
        func.replace(Mission.title, " ", "") == title.replace(" ", ""), 
        func.replace(Mission.description, " ", "") == description.replace(" ", "")
                )
            )
        ).scalars().first()


    if existing_mission:
        return jsonify({"message": "this title or description already exist try another one"}), 400

    if not isinstance(objectives, list):
        return jsonify({"message": "objectives must be a list"}), 400
    
    crew_missions = db.session.execute(select(Mission).where(Mission.crew_owner_id == crew_id, Mission.completed_at.is_(None) )).scalars().all()

    if len(crew_missions) >= 5:
        return jsonify({"message": "crew active missions limit has been reached 5 of 5"}), 400
    
    if len(objectives) > 5:
        return jsonify({"message": "mission objectives must be a maximum of 5"}),400
    
    if len(objectives) < 3:
        return jsonify({"message": f"objectives must be at least 3, {len(objectives)} recieved"}),400
    
    new_mission = Mission(title=title, description=description, creator_id=captain_id, crew_owner_id=crew_id)
    db.session.add(new_mission)
    db.session.commit()


    for objective in objectives:
        new_objective = Objective(title=objective , mission_id =new_mission.id, is_crew=True )
        db.session.add(new_objective)
        db.session.commit()
        
    return jsonify({"mission": new_mission.get_basic_info(), "objectives": new_mission.get_objectives() }),200



# @missions_bp.route("/sailor/<int:sailor_id>", methods=['GET'])
# def get_missions():
#     missions = list(db.session.execute(select(Mission)).scalars().all())

#     return jsonify({"missions": [mission.serialize() for mission in missions]})



# @missions_bp.route("/sailor/<int:sailor_id>", methods=['GET'])
# def get_missions():
#     missions = list(db.session.execute(select(Mission)).scalars().all())

#     return jsonify({"missions": [mission.serialize() for mission in missions]})



# @missions_bp.route("/sailor/<int:sailor_id>", methods=['GET'])
# def get_missions():
#     missions = list(db.session.execute(select(Mission)).scalars().all())

#     return jsonify({"missions": [mission.serialize() for mission in missions]})



# @missions_bp.route("/sailor/<int:sailor_id>", methods=['GET'])
# def get_missions():
#     missions = list(db.session.execute(select(Mission)).scalars().all())

#     return jsonify({"missions": [mission.serialize() for mission in missions]})



# @missions_bp.route("/sailor/<int:sailor_id>", methods=['GET'])
# def get_missions():
#     missions = list(db.session.execute(select(Mission)).scalars().all())

#     return jsonify({"missions": [mission.serialize() for mission in missions]})