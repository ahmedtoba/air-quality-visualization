from datetime import datetime
from app.db_connection import get_database

class AirQualityRepository:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["air_quality_data"]

    def find_by_parameters(self, parameters: list[str], start_date: datetime, end_date: datetime) -> list[dict]:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
        projection = {"timestamp": 1}
        projection.update({param: 1 for param in parameters})
        query = {
            "timestamp": {"$gte": start_date, "$lte": end_date},
            "$and": [{param: {"$exists": True}} for param in parameters]
        }
        return self.collection.find(query, projection)
    
    def find_by_date_range(self, start_date: datetime, end_date: datetime) -> list[dict]:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
        return self.collection.find(
            {"timestamp": {"$gte": start_date, "$lte": end_date}},
        )

    def bulk_insert(self, data_list: list[dict]):
        if not data_list:
            return
        self.collection.insert_many(data_list)

    def get_all_timestamps(self) -> list[dict]:
        return self.collection.find({}, {"timestamp": 1})
