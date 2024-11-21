from flask import Blueprint, request, jsonify
from app.services.data_service import ingest_data, fetch_data
import logging

data_bp = Blueprint('data', __name__)
logger = logging.getLogger(__name__)

@data_bp.post('/upload')
def upload_data():
    """
    Upload Data
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The file to upload
    responses:
      200:
        description: File uploaded successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Data successfully ingested!
      500:
        description: Error occurred during file upload
    """
    try:
        logger.info("Received file upload request.")
        file = request.files['file']
        result = ingest_data(file)
        return jsonify({"message": result})
    except Exception as e:
        logger.error(f"Error in /upload: {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.get('/data')
def get_data():
    """
    Fetch Air Quality Data
    ---
    parameters:
      - name: parameter
        in: query
        type: string
        required: true
        description: The air quality parameter to fetch (e.g., CO, Benzene).
      - name: start_date
        in: query
        type: string
        required: true
        description: Start date for filtering data (YYYY-MM-DD).
      - name: end_date
        in: query
        type: string
        required: true
        description: End date for filtering data (YYYY-MM-DD).
    responses:
      200:
        description: Successfully fetched data
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      timestamp:
                        type: string
                        format: date-time
                      value:
                        type: number
      500:
        description: Error occurred during data fetching
    """
    try:
        logger.info("Received data fetch request.")
        parameter = request.args.get('parameter')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        data = fetch_data(parameter, start_date, end_date)
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in /data: {e}")
        return jsonify({"error": str(e)}), 500

@data_bp.route('/dummy')
def dummy():
    return "Hello, World!"