from datetime import datetime
from app.db_connection import get_database
from app.models.air_quality import AirQualityModel

class AirQualityRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["air_quality_data"]

    def find_by_parameter(self, parameter, start_date, end_date):
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
        return self.collection.find(
            {
                "timestamp": {"$gte": start_date, "$lte": end_date},
                parameter: {"$exists": True},
            },
            {"timestamp": 1, parameter: 1},
        )
    
    def find_by_date_range(self, start_date, end_date):
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
        return self.collection.find(
            {"timestamp": {"$gte": start_date, "$lte": end_date}},
        )

    def bulk_insert(self, data_list):
        if not data_list:
            return
        self.collection.insert_many(data_list)

    def get_all_timestamps(self):
        return self.collection.find({}, {"timestamp": 1})
