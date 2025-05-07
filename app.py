from flask import Flask, request, jsonify
import boto3
import logging
from botocore.exceptions import BotoCoreError, NoCredentialsError

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# AWS S3 client
s3 = boto3.client('s3')

# S3 bucket name
BUCKET_NAME = 'my-file-storage-demo'

@app.route('/')
def home():
    return 'Welcome to Cloud File Storage!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        logging.info(f"Uploaded file: {file.filename}")
        return jsonify({'message': f"File '{file.filename}' uploaded successfully to bucket '{BUCKET_NAME}'"}), 200

    except NoCredentialsError:
        return jsonify({'error': 'AWS credentials not found'}), 500
    except BotoCoreError as e:
        return jsonify({'error': f"Failed to upload file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
