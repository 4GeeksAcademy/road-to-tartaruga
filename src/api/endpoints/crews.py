from flask import Blueprint, jsonify
from api.models import Crew, db
from sqlalchemy import select
import uuid


#Genera codigo de invitacion irrepetible
def generate_invite_code():
    return uuid.uuid4().hex


crews_bp = Blueprint("crews", __name__, url_prefix="crews")

@crews_bp.route("/", methods=['GET'])
def get_crews():
    crews = list(db.session.execute(select(Crew)).scalars().all())

    return jsonify({"crews": [crew.serialize() for crew in crews]})