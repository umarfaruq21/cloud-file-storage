# app.py

from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# AWS S3 Configuration
S3_BUCKET = 'my-file-storage-demo'  # replace with your bucket name
S3_REGION = 'ap-south-1'  # replace with your region if different

# Initialize S3 client
s3 = boto3.client('s3')

@app.route('/')
def home():
    return 'Welcome to the Cloud File Storage App!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        s3.upload_fileobj(file, S3_BUCKET, file.filename)
        return jsonify({'message': f'File {file.filename} uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run on host 0.0.0.0 so it's accessible in EC2
    app.run(host='0.0.0.0', port=5000, debug=True)
