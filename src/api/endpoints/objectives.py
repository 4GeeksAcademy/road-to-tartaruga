from flask import Blueprint , jsonify
from api.extensions import db
from api.models import Sailor, Objective
from sqlalchemy import select

objectives_bp = Blueprint('objectives', __name__, url_prefix="/objectives")

@objectives_bp.route("/sailor/<int:sailor_id>", methods=['GET'])
def get_sailor_objectives(sailor_id):
    
    sailor = db.session.get(Sailor, sailor_id)

    if not sailor:
        return jsonify({"message": "sailor not found"}), 404
    

    return jsonify({"objectives": sailor.get_assigned_objectives()}), 200