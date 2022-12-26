import os

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv, find_dotenv

from parse_pdf import resume_parser

app = Flask(__name__)

load_dotenv(find_dotenv())
port = os.environ.get("FLASK_RUN_PORT")
host = os.environ.get("FLASK_RUN_HOST")

if not os.path.isdir("uploads"):
    os.makedirs("uploads")

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file_extensions(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def main():
    return 'resume parser running'


@app.route('/file-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part

    if 'file' not in request.files:
        resp = jsonify({
            'error': {
                'message': 'File not found'
            }
        })
        resp.status_code = 400
        return resp

    file = request.files['file']

    # check if no file is selected
    if file.filename == '':
        resp = jsonify({
            'error':
                {'message': 'No file selected for uploading'}
        })
        resp.status_code = 400
        return resp

    # check if the file is a PDF
    if file and allowed_file_extensions(file.filename):
        f = request.files['file']
        file_path = os.path.join('.', 'uploads', secure_filename(f.filename))
        f.save(os.path.join(file_path))

        # using resume parser on the PDF file uploaded
        json_file = resume_parser(file_path)
        resp = jsonify(json_file)
        resp.status_code = 201
        # removing the file from the directory
        os.remove(file_path)
        return resp

    else:
        resp = jsonify({
            'error': {
                'message': 'Allowed file type - only pdf'}
        })
        resp.status_code = 400
        return resp


if __name__ == "__main__":
    app.run(host=host, port=port)
