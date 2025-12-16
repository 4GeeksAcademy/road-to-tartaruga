from flask import Blueprint, request, jsonify
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

cloudinary_bp = Blueprint('cloudinary', __name__)


@cloudinary_bp.route("/upload-image", methods=["POST"])
def upload_image():
    
    file = request.files.get("image")
    if not file:
        return jsonify({"message": "none image has been sended"}), 400
    
    try:
        
        result = cloudinary.uploader.upload(
            file, 
            folder="profiles",
            quality="auto",
            fetch_format="auto"
        )

        return jsonify({"secure_url": result["secure_url"],
                        "public_id": result["public_id"]}),200

    except Exception as e:
        return jsonify({"error": str(e)}),500