from flask import Flask, render_template, request, redirect, url_for, flash, json, jsonify
import os
from werkzeug.utils import secure_filename, send_from_directory
import psycopg2
import google.generativeai as genai
from pdf2image import convert_from_path
import json

from api_maneger import api_manager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure Google Gemini API
genai.configure(api_key=api_manager.get_random_api())  # Replace with your actual API key

# Configuration for Gemini model
MODEL_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4906,
}

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=MODEL_CONFIG)

# Ensure upload directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# PostgreSQL Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="157.20.51.93",
        database="adm_db",
        user="postgres",
        password="Vikas$7!5&v^ate@",
        port="9871"
    )
    return conn


# PDF to Image Conversion
def pdf_to_image(pdf_path):
    images = convert_from_path(pdf_path, poppler_path='C:\\Program Files (x86)\\poppler-24.08.0\\Library\\bin')
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(UPLOAD_FOLDER, f"temp_image_{i}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)
    return image_paths


# Image Preparation for API Input
def image_format(image_path):
    with open(image_path, "rb") as img_file:
        return [{"mime_type": "image/png", "data": img_file.read()}]


# Gemini Output Generation
def gemini_output(image_path, system_prompt, user_prompt):
    try:
        image_info = image_format(image_path)
        input_prompt = [system_prompt, image_info[0], user_prompt]
        response = model.generate_content(input_prompt)
        raw_output = response.text.strip()
        if raw_output.startswith("```json"):
            raw_output = raw_output[8:-3].strip()
            print(raw_output)
        return raw_output
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return ""


# Process file and extract data
def process_file(file_path, system_prompt, user_prompt):
    _, file_extension = os.path.splitext(file_path.lower())

    if file_extension == ".pdf":
        image_paths = pdf_to_image(file_path)
        if image_paths:
            output_json = gemini_output(image_paths[0], system_prompt, user_prompt)
        else:
            print("Failed to convert PDF to images.")
            return
    elif file_extension in [".png", ".jpg", ".jpeg"]:
        output_json = gemini_output(file_path, system_prompt, user_prompt)
        print(output_json)
    else:
        print("Unsupported file format.")
        return

    try:
        json_data = json.loads(output_json)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {}


def save_data_to_db(extracted_data):
    conn = None
    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get document type from the extracted data
        document_type = extracted_data.get("documentType")

        # Insert PAN Card data if the document is of type "PAN Card"
        if document_type == "PAN Card":
            cursor.execute(
                """INSERT INTO KYC_Document (documentType, panNumber, name, fatherName, dateOfBirth) VALUES (%s, %s, %s, %s, %s)""",
                (extracted_data.get("documentType"),
                 extracted_data.get("panNumber"),
                 extracted_data.get("name"),
                 extracted_data.get("fatherName"),
                 extracted_data.get("dateOfBirth"))
            )

        # Insert Aadhar Card data if the document is of type "Aadhar Card"
        elif document_type == "Aadhar Card":
            cursor.execute(
                """INSERT INTO KYC_Document (documentType, aadharNumber, name, dateOfBirth, address) VALUES (%s, %s, %s, %s, %s)""",
                (extracted_data.get("documentType"),
                 extracted_data.get("Aadhar Number"),
                 extracted_data.get("Name"),
                 extracted_data.get("dateOfBirth"),
                 extracted_data.get("Address"))
            )

        # Commit transaction
        conn.commit()
        print("Data saved to database successfully.")

    except Exception as e:
        # Print or log the error
        print(f"Error saving data to database: {e}")
        if conn:
            conn.rollback()  # Rollback in case of error

    finally:
        # Ensure the connection is closed
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")




