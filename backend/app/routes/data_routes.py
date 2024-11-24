from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request
from app.logging_config import logger

from app.schemas import AirQualityDataFilterSchema, AirQualityDataResponseSchema, AirQualityDataUploadSchema
from app.services.data_service import AirQualityService

# Create a Blueprint for air quality routes
blp = Blueprint("air_quality_routes", "air_quality", url_prefix="/air-quality")

# Initialize the service
air_quality_service = AirQualityService()


@blp.route("")
class AirQualityListResource(MethodView):
    @blp.arguments(AirQualityDataFilterSchema, location="query")
    @blp.response(200, AirQualityDataResponseSchema(many=True))
    def get(self, query_params):
        start_date = query_params.get("start_date")
        end_date = query_params.get("end_date")
        logger.info(f"Getting data from {start_date} to {end_date}")
        return air_quality_service.get_by_date_range(start_date, end_date), 200
    
@blp.route("/<string:parameter>")
class AirQualityParameterResource(MethodView):
    @blp.response(200, AirQualityDataResponseSchema(many=True))
    @blp.arguments(AirQualityDataFilterSchema, location="query")
    def get(self, parameter, start_date, end_date):
        logger.info(f"Getting data for parameter {parameter} from {start_date} to {end_date}")
        return air_quality_service.get_by_parameter(parameter, start_date, end_date)

@blp.route("/ingest_data")
class AirQualityBulkIngestResource(MethodView):
    @blp.arguments(AirQualityDataUploadSchema, location="files")
    def post(self):
        logger.info("Received CSV file for bulk ingestion")
        file = request.files["file"]
        result = air_quality_service.bulk_ingest_csv(file)
        return {"message": result}, 200
