from flask import Blueprint, jsonify
from api.models import Mission, db
from sqlalchemy import select


missions_bp = Blueprint("missions", __name__, url_prefix="missions")

@missions_bp.route("/", methods=['GET'])
def get_missions():
    missions = list(db.session.execute(select(Mission)).scalars().all())

    return jsonify({"missions": [mission.serialize() for mission in missions]})