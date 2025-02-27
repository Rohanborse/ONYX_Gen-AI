from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from KYC_doc.kyc_main import process_file
from api_maneger import system_prompt_Adhar, system_prompt_pan, user_prompt_pan, user_prompt_Adhar
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# File Upload & Processing for PAN Card
@app.route('/upload_pan', methods=['POST'])
def upload_pan():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    extracted_data = process_file(filepath, system_prompt_pan, user_prompt_pan)
    if extracted_data and extracted_data.get("documentType") == "PAN Card":
        return jsonify({'message': 'PAN Card processed successfully', 'data': extracted_data}), 200
    return jsonify({'error': 'Invalid PAN Card data'}), 400

# File Upload & Processing for Aadhar Card
@app.route('/upload_aadhar', methods=['POST'])
def upload_aadhar():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    extracted_data = process_file(filepath, system_prompt_Adhar, user_prompt_Adhar)
    if extracted_data and extracted_data.get("documentType") == "Aadhar Card":
        return jsonify({'message': 'Aadhar Card processed successfully', 'data': extracted_data}), 200
    return jsonify({'error': 'Invalid Aadhar Card data'}), 400


if __name__ == '__main__':
    app.run(debug=True)
