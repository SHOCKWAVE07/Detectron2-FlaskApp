from flask import Blueprint, render_template, request, send_from_directory
from app.utils import perform_instance_segmentation
import base64

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle image upload and perform instance segmentation
        result_image = perform_instance_segmentation(request.files['image'], output_format='png')

        return render_template('index.html', result_image=result_image)

    return render_template('index.html')

@main_bp.route('/segment', methods=['POST'])
def segment():
    if 'image' in request.files:
        result_image = perform_instance_segmentation(request.files['image'], output_format='png')
        return result_image
    else:
        return "No image received"

@main_bp.route('/static/<path:filename>')
def download_file(filename):
<<<<<<< Updated upstream
    return send_from_directory('static', filename)
=======
    return send_from_directory('static', filename)
>>>>>>> Stashed changes
