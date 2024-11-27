from dataclasses import asdict
from io import TextIOWrapper
import csv
from datetime import datetime
from app.repositories.air_quality_repository import AirQualityRepository
from app.models.air_quality import AirQualityModel
from app.logging_config import logger


class AirQualityService:
    def __init__(self):
        self.repository = AirQualityRepository()

    def get_by_parameters(self, parameters: list[str], start_date: datetime, end_date: datetime) -> list[dict]: 
        return self.repository.find_by_parameters(parameters, start_date, end_date)
    
    def get_by_date_range(self, start_date, end_date):
        logger.info(f"Getting data from {start_date} to {end_date}")
        return self.repository.find_by_date_range(start_date, end_date)

    def bulk_ingest_csv(self, file):
        data = self._process_csv(file)

        existing_timestamps = set(
            record["timestamp"] for record in self.repository.get_all_timestamps()
        )
        unique_data = [row for row in data if row["timestamp"] not in existing_timestamps]

        # Bulk insert unique data
        self.repository.bulk_insert(unique_data)
        return f"{len(unique_data)} rows successfully ingested, {len(data) - len(unique_data)} duplicates ignored."
    
    def _process_csv(self, file) -> list[dict]:
        logger.info("Processing CSV file...")
        csv_data = []
        reader = csv.DictReader(TextIOWrapper(file, encoding="utf-8"), delimiter=";")

        for row in reader:
            try:
                if not row.get("Date") or not row.get("Time"):
                    logger.error(f"Missing Date or Time in row: {row}")
                    continue

                parsed_row = AirQualityModel(
                    timestamp=datetime.strptime(f"{row['Date']} {row['Time']}", "%d/%m/%Y %H.%M.%S"),
                    CO_GT=float(row.get("CO(GT)", 0).replace(",", ".")),
                    PT08_S1_CO=float(row.get("PT08.S1(CO)", 0).replace(",", ".")),
                    NMHC_GT=float(row.get("NMHC(GT)", 0).replace(",", ".")),
                    C6H6_GT=float(row.get("C6H6(GT)", 0).replace(",", ".")),
                    PT08_S2_NMHC=float(row.get("PT08.S2(NMHC)", 0).replace(",", ".")),
                    NOx_GT=float(row.get("NOx(GT)", 0).replace(",", ".")),
                    PT08_S3_NOx=float(row.get("PT08.S3(NOx)", 0).replace(",", ".")),
                    NO2_GT=float(row.get("NO2(GT)", 0).replace(",", ".")),
                    PT08_S4_NO2=float(row.get("PT08.S4(NO2)", 0).replace(",", ".")),
                    PT08_S5_O3=float(row.get("PT08.S5(O3)", 0).replace(",", ".")),
                    T=float(row.get("T", 0).replace(",", ".")),
                    RH=float(row.get("RH", 0).replace(",", ".")),
                    AH=float(row.get("AH", 0).replace(",", ".")),
                )
                csv_data.append(asdict(parsed_row))
            except Exception as e:
                logger.error(f"Error parsing row: {row}, {e}")

        return csv_data

    def get_all_timestamps(self):
        return self.repository.get_all_timestamps()
            

