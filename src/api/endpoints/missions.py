from flask import Blueprint, jsonify, request
from api.models import Mission, db, Sailor, Crew, Objective, CrewSailor, Contribution, ClaudeMission
from sqlalchemy import select, func, or_
from datetime import datetime, timezone, time
from zoneinfo import ZoneInfo

missions_bp = Blueprint("missions", __name__, url_prefix="/missions")


@missions_bp.route("/<int:mission_id>")
def get_mission(mission_id):

    mission = db.session.get(Mission, mission_id)

    if not mission:
        return jsonify({"message": "mission not found"}),404

    return jsonify(mission.get_basic_info()),200


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
    description = body.get("description")
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



@missions_bp.route("/sailor/<int:sailor_id>/<int:mission_id>", methods=['PATCH'])
def edit_sailor_mission(sailor_id, mission_id):

    sailor = db.session.get(Sailor,sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found"}), 404
    
    mission = db.session.execute(select(Mission).where(Mission.sailor_owner_id == sailor_id, Mission.id == mission_id)).scalars().first()

    if not mission:
        return jsonify({"message": "mission not found"})
    
    body = request.get_json()
    title = body.get("title")
    description = body.get("description")

    formatted_title = title.replace(" ", "").lower()
    formatted_description = description.replace(" ", "").lower()

    if formatted_title == "" or formatted_description == "":
        return jsonify({"message": "title and description must send something, even if is the previous value"}),400
    
    if not title and not description:
        return jsonify({"message": "title or description are required fields"}),400

    existing_mission = db.session.execute(select(Mission).where(or_(
            func.replace(Mission.title, " ", "") == title.replace(" ", ""),
            func.replace(Mission.description, " ", "") == description.replace(" ", "")
          ), Mission.id != mission_id)).scalars().first()

    if existing_mission:
        return jsonify({"message": "title or description already exist, try another one"}), 400
    
    if mission.title.replace(" ", "").lower() != title.replace(" ", "").lower():
        mission.title = title
    if mission.description.replace(" ", "").lower() != description.replace(" ", "").lower():
        mission.description = description
    db.session.commit()

    return jsonify({"mission" : mission.get_basic_info()})
    







@missions_bp.route("/crew/<int:crew_id>/mission/<int:mission_id>/<int:sailor_id>", methods=['PATCH'])
def edit_crew_mission(mission_id, sailor_id, crew_id):
   
    sailor = db.session.get(Sailor,sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found"}), 404
    
    crew = db.session.get(Crew, crew_id)

    if not crew:
        return jsonify({"message": "crew not found"}), 404
    
    mission = db.session.execute(select(Mission).where(Mission.crew_owner_id == crew_id, Mission.id == mission_id)).scalars().first()

    if not mission:
        return jsonify({"message": "mission not found"})


    crew_sailor = db.session.execute(select(CrewSailor).where(CrewSailor.sailor_id == sailor_id, CrewSailor.crew_id == crew_id)).scalars().first()

    if not crew_sailor:
        return jsonify({"message": "this sailor is not part of the crew"}), 400

    if not crew_sailor.is_captain:
        return jsonify({"message": "this sailor is not captain"}), 400
    
    
    body = request.get_json()
    title = body.get("title")
    description = body.get("description")

    if not title and not description:
        return jsonify({"message": "title or description are required fields"}),400
    
    formatted_title = title.replace(" ", "").lower()
    formatted_description = description.replace(" ", "").lower()

    if formatted_title == "" or formatted_description == "":
        return jsonify({"message": "title and description must send something, even if is the previous value"}),400
    

    existing_mission = db.session.execute(select(Mission).where(or_(
            func.replace(Mission.title, " ", "") == title.replace(" ", ""),
            func.replace(Mission.description, " ", "") == description.replace(" ", "")
          ), Mission.id != mission_id)).scalars().first()

    if existing_mission:
        return jsonify({"message": "title or description already exist, try another one"}), 400
    
    if mission.title.replace(" ", "").lower() != title.replace(" ", "").lower():
        mission.title = title
    if mission.description.replace(" ", "").lower() != description.replace(" ", "").lower():
        mission.description = description
    db.session.commit()

    return jsonify({"mission" : mission.get_basic_info()})




@missions_bp.route("/sailor/<int:sailor_id>/mission/<int:mission_id>", methods=['DELETE'])
def delete_sailor_mission(sailor_id, mission_id):
   
    sailor = db.session.get(Sailor,sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found"}), 404

    mission = db.session.execute(select(Mission).where(Mission.sailor_owner_id == sailor_id, Mission.id == mission_id)).scalars().first()

    if not mission:
        return jsonify({"message": "mission not found"})
    
    db.session.delete(mission)

    db.session.commit()

    return jsonify({"done": True}), 200






@missions_bp.route("/crew/<int:crew_id>/mission/<int:mission_id>/<int:sailor_id>", methods=['DELETE'])
def delete_crew_mission(sailor_id, mission_id, crew_id):
   
    sailor = db.session.get(Sailor,sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found"}), 404
    
    crew = db.session.get(Crew, crew_id)

    if not crew:
        return jsonify({"message": "crew not found"}), 404
    
    crew_sailor = db.session.execute(select(CrewSailor).where(CrewSailor.sailor_id == sailor_id, CrewSailor.crew_id == crew_id)).scalars().first()

    if not crew_sailor:
        return jsonify({"message": "this sailor is not part of the crew"}), 400

    if not crew_sailor.is_captain:
        return jsonify({"message": "this sailor is not captain"}), 400
    

    mission = db.session.execute(select(Mission).where(Mission.crew_owner_id == crew_id, Mission.id == mission_id)).scalars().first()

    if not mission:
        return jsonify({"message": "mission not found"})
    
    db.session.delete(mission)

    db.session.commit()

    return jsonify({"done": True}), 200









@missions_bp.route("/sailor/<int:sailor_id>/mission/<int:mission_id>/complete/claude-mission/<int:cm_id>", methods=['PATCH'])
def complete_sailor_mission(sailor_id, mission_id, cm_id):

    sailor = db.session.get(Sailor,sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found"}), 404

    mission = db.session.execute(select(Mission).where(Mission.sailor_owner_id == sailor_id, Mission.id == mission_id)).scalars().first()

    if not mission:
        return jsonify({"message": "mission not found"})
    
    objectives = db.session.execute(select(Objective).where(Objective.mission_id == mission_id)).scalars().all()
    completed_objectives = db.session.execute(select(Objective).where(Objective.mission_id == mission_id, Objective.completed_at != None)).scalars().all()
    
    
    if len(objectives) != len(completed_objectives):
        return jsonify({"message": "you need to complete all the objectives"}), 400

    
    es = ZoneInfo("Europe/Madrid")

    today = datetime.now(es).date()

    day_start = datetime.combine(today, time.min, tzinfo=es)
    day_end = datetime.combine(today, time.max, tzinfo=es)

    utc_day_start = day_start.astimezone(ZoneInfo("UTC"))
    utc_day_end = day_end.astimezone(ZoneInfo("UTC"))


    
    completed_today = db.session.execute(
        select(Mission).where(Mission.sailor_owner_id == sailor_id,
                              Mission.id == mission_id,
                              Mission.completed_at >= utc_day_start,
                              Mission.completed_at <= utc_day_end
                              )
    ).scalars().all()

    if(len(completed_today) >= 3):
        return jsonify({"message": "maximum of diary mission completed reached 3 of 3"}), 400
    
    if mission.completed_at is not None:
        return jsonify({"message": "mission already completed"}),400
    

    claude_mission = db.session.execute(select(ClaudeMission).where(ClaudeMission.id == cm_id)).scalars().first()

    if not claude_mission:
        return jsonify({"message": "claude_mission not found"}),404

    contribution = db.session.execute(select(Contribution).where(Contribution.sailor_id == sailor_id, Contribution.claude_mission_id == cm_id)).scalars().first()
    
    if not contribution:
        new_contribution = Contribution(sailor_id=sailor_id, claude_mission_id = cm_id, is_crew=True, contribution=2)
        db.session.add(new_contribution)

    else:
        contribution.contribution = contribution.contribution + 2
    
    mission.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({"mission": mission.get_basic_info()}), 200








@missions_bp.route("/crew/<int:crew_id>/mission/<int:mission_id>/<int:sailor_id>/complete/claude-mission/<int:cm_id>", methods=['PATCH'])
def complete_crew_mission(sailor_id, mission_id, crew_id, cm_id):

    sailor = db.session.get(Sailor,sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found"}), 404
    
    crew = db.session.get(Crew, crew_id)

    if not crew:
        return jsonify({"message": "crew not found"}), 404
    
    mission = db.session.execute(select(Mission).where(Mission.crew_owner_id == crew_id, Mission.id == mission_id)).scalars().first()


    if not mission:
        return jsonify({"message": "mission not found"})


    crew_sailor = db.session.execute(select(CrewSailor).where(CrewSailor.sailor_id == sailor_id, CrewSailor.crew_id == crew_id)).scalars().first()


    if not crew_sailor:
        return jsonify({"message": "this sailor is not part of the crew"}), 400

    if not crew_sailor.is_captain:
        return jsonify({"message": "this sailor is not captain"}), 400

    
    es = ZoneInfo("Europe/Madrid")

    today = datetime.now(es).date()

    day_start = datetime.combine(today, time.min, tzinfo=es)
    day_end = datetime.combine(today, time.max, tzinfo=es)

    utc_day_start = day_start.astimezone(ZoneInfo("UTC"))
    utc_day_end = day_end.astimezone(ZoneInfo("UTC"))


    completed_today = db.session.execute(
        select(Mission).where(Mission.crew_owner_id == crew_id,
                              Mission.id == mission_id,
                              Mission.completed_at >= utc_day_start,
                              Mission.completed_at <= utc_day_end
                              )
    ).scalars().all()

    if(len(completed_today) >= 5):
        return jsonify({"message": "maximum of diary mission completed reached, 5 of 5"}), 400



    if mission.completed_at is not None:
        return jsonify({"message": "mission is already completed"}),400
    
    claude_mission = db.session.execute(select(ClaudeMission).where(ClaudeMission.id == cm_id)).scalars().first()

    if not claude_mission:
        return jsonify({"message": "claude_mission not found"}),404

    contribution = db.session.execute(select(Contribution).where(Contribution.crew_id == crew_id, Contribution.claude_mission_id == cm_id)).scalars().first()
    
    if not contribution:
        new_contribution = Contribution(crew_id=crew_id, claude_mission_id = cm_id, is_crew=True, contribution=10)
        db.session.add(new_contribution)

    else:
        contribution.contribution = contribution.contribution + 10
    mission.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({"mission": mission.get_basic_info()}), 200


