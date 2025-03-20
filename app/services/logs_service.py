from flask import Blueprint, jsonify, send_from_directory, url_for
import os

# Criar a blueprint
logs_bp = Blueprint('logs', __name__)

# Defina a pasta logs
LOGS_DIR = 'logs'

@logs_bp.route('/', methods=['GET'])
def list_logs():
    try:
        files = os.listdir(LOGS_DIR)
        # Gerar links para download
        files_with_links = [
            {"filename": file, "download_link": url_for('logs.download_log', filename=file, _external=True)}
            for file in files
        ]
        return jsonify(files_with_links)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@logs_bp.route('/<filename>', methods=['GET'])
def download_log(filename):
    try:
        return send_from_directory(LOGS_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
