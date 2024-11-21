import logging
import pandas as pd

logger = logging.getLogger(__name__)

def ingest_data(file):
    from app import mongo
    try:
        logger.info("Starting data ingestion.")
        data = pd.read_excel(file)
        records = data.to_dict(orient='records')
        mongo.db.air_quality.insert_many(records)
        logger.info(f"Ingested {len(records)} records successfully.")
        return "Data successfully ingested!"
    except Exception as e:
        logger.error(f"Error during data ingestion: {e}")
        raise

def fetch_data(parameter, start_date, end_date):
    from app import mongo
    try:
        logger.info(f"Fetching data for parameter: {parameter} from {start_date} to {end_date}.")
        query = {}
        if start_date and end_date:
            query["timestamp"] = {"$gte": start_date, "$lte": end_date}

        projection = {"_id": 0}
        if parameter:
            projection[parameter] = 1
            projection["timestamp"] = 1

        results = mongo.db.air_quality.find(query, projection)
        logger.info(f"Fetched {len(results)} records.")
        return list(results)
    except Exception as e:
        logger.error(f"Error during data fetch: {e}")
        raise

def seed_data():
    from app import mongo
    """
    Seeds the database with initial data from the dataset file if no data exists.
    """
    try:
        # Check if the collection is empty
        if mongo.db.air_quality.count_documents({}) > 0:
            logger.info("Database already seeded.")
            return "Database already seeded."

        # Load dataset from Excel
        dataset_path = "dataset/AirQualityUCI.xlsx"  # Adjust the path if needed
        data = pd.read_excel(dataset_path)

        # Prepare data for MongoDB
        records = data.to_dict(orient="records")

        # Insert data into MongoDB
        mongo.db.air_quality.insert_many(records)
        logger.info("Database seeded successfully.")
        return "Database seeded successfully."
    except Exception as e:
        logger.error(f"Error seeding data: {e}")
        raise Exception(f"Error seeding data: {e}")