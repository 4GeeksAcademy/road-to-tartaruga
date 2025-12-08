from flask import Blueprint, request, jsonify
from sqlalchemy import select
from api.extensions import db
from api.models import CrewSailor, CrewSailorStatus, Crew, Sailor

crew_sailors_bp = Blueprint('crew_sailors', __name__, url_prefix='/crew_sailors')


@crew_sailors_bp.route("/", methods=['GET'])
def get_crew_sailor():

    crew_sailor_id = request.args.get("crew_sailor_id", None)
    if not crew_sailor_id:
        crew_id = request.args.get("crew_id", None)
        sailor_id = request.args.get("sailor_id", None)

        for key in ["crew_id", "sailor_id"]:
            if not key in request.args:
                return jsonify({"message" : f"{key} field is missing"}), 400
            
        crew = db.session.get(Crew, crew_id)
        if not crew:
            return jsonify({"message": "crew not found"}),404
        
        sailor = db.session.get(Sailor, sailor_id)
        if not sailor:
            return jsonify({"message": "sailor not found"}),404
        
        crew_sailor = db.session.execute(select(CrewSailor).where(CrewSailor.crew_id == crew_id, CrewSailor.sailor_id == sailor_id)).scalars().first()

        if not crew_sailor:
            return jsonify({"message": "crew_sailor not found"}), 404


        return jsonify({"crew_sailor": crew_sailor.serialize()}), 200
    
    crew_sailor = db.session.execute(select(CrewSailor).where(CrewSailor.id == crew_sailor_id)).scalars().first()

    if not crew_sailor:
        return jsonify({"message": "crew_sailor not found"}), 404
    
    return jsonify({"crew_sailor": crew_sailor.serialize()}), 200




@crew_sailors_bp.route("/<int:sailor_id>/active", methods=['POST'])
def create_crew_sailor(sailor_id):

    code = request.get_json().get("code", None)
    
    if not code:
        return jsonify({"message": "code field is missing"}), 400
    
    crew = db.session.execute(select(Crew).where(Crew.code == code)).scalars().first()

    if not crew:
        return jsonify({"message": "invalid crew code"}), 404
    
    crew_id = crew.id
    
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
        

    crew_cs = db.session.execute(select(CrewSailor).where(CrewSailor.crew_id == crew_id)).scalars().all()

    crew_cs_counter = len(crew_cs)

    sailor_cs = db.session.execute(select(CrewSailor).where(CrewSailor.sailor_id == sailor_id)).scalars().all()

    sailor_cs_counter = len(sailor_cs)

    if crew_cs_counter >= 5:
        return jsonify({"message": "limit of crew_sailors for this crew has been reached, 5 of 5"}), 400
    
    if sailor_cs_counter >= 3:
        return jsonify({"message": "limit of crew_sailor for this sailor has been reached, 3 of 3"})
    

    new_cs = CrewSailor(sailor_id = sailor_id, crew_id = crew_id)

    db.session.add(new_cs)
    db.session.commit()

    return jsonify(new_cs.serialize())
    


    


@crew_sailors_bp.route("/<int:cs_id>/inactive", methods=['PATCH'])
def inactive_crew_sailor(cs_id):
    
    cs = db.session.get(CrewSailor, cs_id)

    if not cs:
        return jsonify({"message": "crew_sailor not found"}), 404
    
    if cs.status == CrewSailorStatus.ACTIVE:
        cs.status = CrewSailorStatus.INACTIVE
        db.session.commit()
        return jsonify({"message": "crew_sailor was sucessfully inactivated"}), 200

    return jsonify({"message": "crew_sailor cannot be inactivated"}), 400



@crew_sailors_bp.route("/<int:cs_id_from>/<int:cs_id_to>/kick", methods=['PATCH'])
def kick_crew_sailor(cs_id_from, cs_id_to):
     
    cs_to = db.session.get(CrewSailor, cs_id_to)

    if not cs_to:
        return jsonify({"message": "crew_sailor not found"}), 404
    
    cs_from = db.session.get(CrewSailor, cs_id_from)

    if not cs_from.is_captain:
        return jsonify({
            "message": "just a captain can kick a sailor from the boat"
        }), 401

    
    if cs_to.status != CrewSailorStatus.KICKED:
        cs_to.status = CrewSailorStatus.KICKED
        return jsonify({"message": "crew_sailor was sucessfully kicked"}), 200

    return jsonify({"message": "crew_sailor is already kicked"}), 400




@crew_sailors_bp.route("/<int:cs_id>/captain", methods=['PATCH'])
def captain_crew_sailor(crew_sailor_id):
    crew_sailor_id = request.args.get("crew_sailor_id")
    crew_sailor = db.session.get(CrewSailor, crew_sailor_id)
    if not crew_sailor_id:
        return jsonify({"message": "crew_sailor not found"}), 404
    pass