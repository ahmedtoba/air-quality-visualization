from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request
from app.logging_config import logger
from app.schemas import AirQualityDataFilterSchema, AirQualityDataResponseSchema, AirQualityDataUploadSchema
from app.services.data_service import AirQualityService

blp = Blueprint("air_quality_routes", "air_quality")
air_quality_service = AirQualityService()

@blp.route("")
class AirQualityListResource(MethodView):
    @blp.doc(description=
        """
        Get air quality data by date range
        """
    )
    @blp.arguments(AirQualityDataFilterSchema, location="query")
    @blp.response(200, AirQualityDataResponseSchema(many=True))
    def get(self, query_params):
        start_date = query_params["start_date"]
        end_date = query_params["end_date"]
        logger.info(f"Getting data from {start_date} to {end_date}")
        return air_quality_service.get_by_date_range(start_date, end_date), 200
    
@blp.route("/<string:parameter>")
class AirQualityParameterResource(MethodView):
    @blp.arguments(AirQualityDataFilterSchema, location="query")
    # I need to add documentation for the parameter argument which is inisde the route
    @blp.doc(description=
        """
        Get air quality data by parameter and date range
        Possible parameters: CO_GT, PT08_S1_CO, NMHC_GT, C6H6_GT, PT08_S2_NMHC, NOx_GT, PT08_S3_NOx, NO2_GT, PT08_S4_NO2, PT08_S5_O3, T, RH, AH
        """
    )
    @blp.response(200, AirQualityDataResponseSchema(many=True))
    def get(self, query_params, parameter):
        start_date = query_params["start_date"]
        end_date = query_params["end_date"]
        logger.info(f"Getting data for parameter {parameter} from {start_date} to {end_date}")
        return air_quality_service.get_by_parameter(parameter, start_date, end_date)

@blp.route("/ingest_data")
class AirQualityBulkIngestResource(MethodView):
    @blp.doc(description=
        """
        Bulk ingest air quality data from a CSV file
        """
    )
    @blp.arguments(AirQualityDataUploadSchema, location="files")
    def post(self, file):
        logger.info("Received CSV file for bulk ingestion")
        file = request.files["file"]
        result = air_quality_service.bulk_ingest_csv(file)
        return {"message": result}, 200
