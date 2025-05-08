from flask import Flask, request
import boto3

app = Flask(__name__)
s3 = boto3.client('s3')

BUCKET_NAME = 'my-file-storage-demo'

@app.route('/')
def home():
    return "Welcome to Cloud File Storage!"

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    s3.upload_fileobj(file, BUCKET_NAME, file.filename)
    return f"File {file.filename} uploaded successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
