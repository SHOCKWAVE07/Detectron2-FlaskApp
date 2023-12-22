from flask import Blueprint, request, send_from_directory, send_file
from app.utils import perform_instance_segmentation

main_bp = Blueprint('main', __name__)

@main_bp.route('/segment', methods=['POST'])
def segment():
    if 'image' in request.files:
        # Handle image upload and perform instance segmentation
        result_image = perform_instance_segmentation(request.files['image'], output_format='png')

        # Return image bytes
        return result_image
    else:
        return "No image received"

@main_bp.route('/static/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename)
