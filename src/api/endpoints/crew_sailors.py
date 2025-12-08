from flask import Blueprint, request, jsonify
from sqlalchemy import select
from api.extensions import db
from api.models import CrewSailor, CrewSailorStatus, Crew

crew_sailors_bp = Blueprint('crew_sailors', __name__, url_prefix='/crew_sailors')


@crew_sailors_bp.rout("/<int:sailor_id>", methods=['POST'])
def create_crew_sailor(crew_id, sailor_id):

    code = request.get_json().get("code", None)
    
    if not code:
        return jsonify({"message": "code field is missing"}), 400
    
    cs = db.session.execute(select(Crew).where(Crew.code == code)).scalars().first()

    if not cs:
        return jsonify({"message": "invalid crew code"}), 404
    
    crew_id = cs.id
    
    exist_cs = db.session.execute(select(CrewSailor).where(CrewSailor.sailor_id == sailor_id, CrewSailor.crew_id == crew_id)).scalars().first()

    if exist_cs:
        if exist_cs.status == CrewSailorStatus.ACTIVE:
            return jsonify({"message": "this crew_sailor already is active"}), 409
        
        if exist_cs.status == CrewSailorStatus.INACTIVE:
            exist_cs.status = CrewSailorStatus.ACTIVE
            db.session.commit()
            return jsonify({"message": "this crew_sailor was successfully activated"}), 200
        

        if exist_cs.status == CrewSailorStatus.KICKED:
            return jsonify({"message": "this crew_sailor is kicked, to join the crew the captain must re-admit it"}), 409
        

    
    


    


@crew_sailors_bp.rout("/inactive", methods=['PATCH'])
def inactive_crew_sailor():
    crew_sailor_id = request.args.get("crew_sailor_id")
    crew_sailor = db.session.get(CrewSailor, crew_sailor_id)
    if not crew_sailor_id:
        return jsonify({"message": "crew_sailor not found"}), 404
    pass

@crew_sailors_bp.rout("/active", methods=['PATCH'])
def active_crew_sailor():
    crew_sailor_id = request.args.get("crew_sailor_id")
    crew_sailor = db.session.get(CrewSailor, crew_sailor_id)
    if not crew_sailor_id:
        return jsonify({"message": "crew_sailor not found"}), 404
    pass

@crew_sailors_bp.rout("/kick", methods=['PATCH'])
def kick_crew_sailor():
    crew_sailor_id = request.args.get("crew_sailor_id")
    crew_sailor = db.session.get(CrewSailor, crew_sailor_id)
    if not crew_sailor_id:
        return jsonify({"message": "crew_sailor not found"}), 404
    pass

@crew_sailors_bp.rout("/captain", methods=['PATCH'])
def captain_crew_sailor():
    crew_sailor_id = request.args.get("crew_sailor_id")
    crew_sailor = db.session.get(CrewSailor, crew_sailor_id)
    if not crew_sailor_id:
        return jsonify({"message": "crew_sailor not found"}), 404
    pass