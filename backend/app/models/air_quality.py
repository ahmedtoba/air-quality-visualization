from dataclasses import dataclass
from datetime import datetime
from app.db_connection import get_database

@dataclass
class AirQualityModel:
    timestamp: datetime
    CO_GT: float
    PT08_S1_CO: float
    NMHC_GT: float
    C6H6_GT: float
    PT08_S2_NMHC: float
    NOx_GT: float
    PT08_S3_NOx: float
    NO2_GT: float
    PT08_S4_NO2: float
    PT08_S5_O3: float
    T: float
    RH: float
    AH: float