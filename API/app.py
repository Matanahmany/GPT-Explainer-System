from flask import Flask, request, jsonify
import os
import uuid
import datetime
from pathlib import Path
import json
import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Any

TIME_FORMAT = '%Y-%m-%d-%H-%M-%S'

NOT_FOUND = 404
OK = 200
BAD_REQUEST = 400

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
LOG_FOLDER = 'logs'

Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
Path(LOG_FOLDER).mkdir(parents=True, exist_ok=True)

# Set up logging
handler = TimedRotatingFileHandler(
    os.path.join(LOG_FOLDER, "server.log"), when="midnight", interval=1, backupCount=5
)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


def generate_unique_filename(original_filename: str, uid: str) -> str:
    """Generate a unique filename with timestamp and UID."""
    timestamp = datetime.datetime.now().strftime(TIME_FORMAT)
    return f"{timestamp}_{uid}_{original_filename}"


@app.route('/upload', methods=['POST'])
def upload_file() -> Any:
    """Handle file upload and return UID."""
    if 'file' not in request.files:
        app.logger.error("No file part in the request")
        return jsonify({"error": "No file part in the request"}), BAD_REQUEST
    file = request.files['file']
    if file.filename == '':
        app.logger.error("No selected file")
        return jsonify({"error": "No selected file"}), BAD_REQUEST

    uid = str(uuid.uuid4())
    filename = generate_unique_filename(file.filename, uid)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    app.logger.info(f"File uploaded: {filename}")
    return jsonify({"uid": uid}), OK


@app.route('/status/<uid>', methods=['GET'])
def check_status(uid: str) -> Any:
    """Check the processing status of a file by its UID."""
    metadata = {
        "status": "not found",
        "filename": None,
        "timestamp": None,
        "explanation": None
    }
    upload_filename = [filename for filename in os.listdir(UPLOAD_FOLDER) if filename.split('_')[1] == uid]
    output_filename = [filename for filename in os.listdir(OUTPUT_FOLDER) if filename.split('_')[1] == uid]

    if upload_filename:
        file_split_in_upload = upload_filename[0].split('_')
        metadata["status"] = "pending"
        metadata["filename"] = file_split_in_upload[2]
        metadata["timestamp"] = file_split_in_upload[0]
        app.logger.info(f"Status checked for UID {uid}: pending")
        return jsonify(metadata), OK

    elif output_filename:
        file_split_in_output = output_filename[0].split('_')
        metadata["status"] = "done"
        metadata["filename"] = file_split_in_output[2].rsplit('.', 1)[0]
        metadata["timestamp"] = file_split_in_output[0]
        output_path = os.path.join(OUTPUT_FOLDER, output_filename[0])
        with open(output_path, 'r') as output_file:
            metadata["explanation"] = json.load(output_file)
        app.logger.info(f"Status checked for UID {uid}: done")
        return jsonify(metadata), OK

    else:
        app.logger.error(f"Status check for UID {uid}: not found")
        return jsonify(metadata), NOT_FOUND


if __name__ == "__main__":
    app.run(debug=True)
