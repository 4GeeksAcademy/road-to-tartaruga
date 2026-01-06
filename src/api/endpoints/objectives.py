from flask import Blueprint , jsonify
from api.extensions import db
from datetime import datetime, timezone
from api.models import Sailor, Objective
from sqlalchemy import select

objectives_bp = Blueprint('objectives', __name__, url_prefix="/objectives")

@objectives_bp.route("/sailor/<int:sailor_id>", methods=['GET'])
def get_sailor_objectives(sailor_id):
    
    sailor = db.session.get(Sailor, sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found"}), 404
    

    return jsonify({"objectives": sailor.get_assigned_objectives()}), 200






@objectives_bp.route("/<int:objective_id>/complete", methods=['PATCH'])
def complete_objective(objective_id):

    objective = db.session.get(Objective, objective_id)

    if not objective:
        return jsonify({"message": "objective not found"}),404
    
    if objective.completed_at:
        objective.completed_at = None
    else:
        objective.completed_at = datetime.now(timezone.utc)
        
    db.session.commit()
    
    return jsonify(objective.get_info_for_mission()), 200