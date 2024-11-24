from io import StringIO
from app.services.data_service import AirQualityService
from app.repositories.air_quality_repository import AirQualityRepository
from app.models.air_quality import AirQualityModel
from datetime import datetime
from unittest.mock import MagicMock, patch

def test_get_by_parameter(mocker):
    # Arrange
    mock_repository = mocker.patch("app.services.data_service.AirQualityRepository")
    service = AirQualityService()
    mock_repository.return_value.find_by_parameter.return_value = [{
        "timestamp": "2004-03-10T00:00:00", "CO_GT": 1.2
    }]

    # Act
    result = service.get_by_parameter("CO_GT", datetime(2004, 3, 10), datetime(2004, 3, 20))

    # Assert
    assert result == [{"timestamp": "2004-03-10T00:00:00", "CO_GT": 1.2}]

def test_get_by_date_range(mocker):
    # Arrange
    mock_repository = mocker.patch("app.services.data_service.AirQualityRepository")
    service = AirQualityService()
    mock_repository.return_value.find_by_date_range.return_value = [{
        "timestamp": "2004-03-10T00:00:00", "CO_GT": 1.2, "PT08_S1_CO": 2.3, 
        "NMHC_GT": 3.4, "C6H6_GT": 4.5, "PT08_S2_NMHC": 5.6, "NOx_GT": 6.7, 
        "PT08_S3_NOx": 7.8, "NO2_GT": 8.9, "PT08_S4_NO2": 9.0, "PT08_S5_O3": 10.1, 
        "T": 11.2, "RH": 12.3, "AH": 13.4
    }]

    # Act
    result = service.get_by_date_range(datetime(2004, 3, 10), datetime(2004, 3, 20))

    # Assert
    assert result == [{
        "timestamp": "2004-03-10T00:00:00", "CO_GT": 1.2, "PT08_S1_CO": 2.3, 
        "NMHC_GT": 3.4, "C6H6_GT": 4.5, "PT08_S2_NMHC": 5.6, "NOx_GT": 6.7, 
        "PT08_S3_NOx": 7.8, "NO2_GT": 8.9, "PT08_S4_NO2": 9.0, "PT08_S5_O3": 10.1, 
        "T": 11.2, "RH": 12.3, "AH": 13.4
    }]

def test_bulk_ingest_csv(mocker):
    # Arrange
    mock_repository = mocker.patch("app.services.data_service.AirQualityRepository")
    service = AirQualityService()
    mock_repository.return_value.get_all_timestamps.return_value = [{"timestamp": "2004-03-10T00:00:00"}]
    mock_repository.return_value.bulk_insert.return_value = None

    mock_csv = StringIO("Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);NOx(GT);PT08.S3(NOx);NO2(GT);PT08.S4(NO2);PT08.S5(O3);T;RH;AH\n"
                        "10/03/2004;00.00.00;1.2;2.3;3.4;4.5;5.6;6.7;7.8;8.9;9.0;10.1;11.2;12.3;13.4")

    mocker.patch("app.services.data_service.csv.DictReader", return_value=[
        {"Date": "10/03/2004", "Time": "00.00.00", "CO(GT)": "1.2", "PT08.S1(CO)": "2.3", "NMHC(GT)": "3.4", "C6H6(GT)": "4.5", 
         "PT08.S2(NMHC)": "5.6", "NOx(GT)": "6.7", "PT08.S3(NOx)": "7.8", "NO2(GT)": "8.9", "PT08.S4(NO2)": "9.0", "PT08.S5(O3)": "10.1", 
         "T": "11.2", "RH": "12.3", "AH": "13.4"}
    ])

    # Act
    result = service.bulk_ingest_csv(mock_csv)

    # Assert
    assert result == "1 rows successfully ingested, 0 duplicates ignored."

def test_process_csv(mocker):
    # Arrange
    service = AirQualityService()
    mock_csv = StringIO("Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);NOx(GT);PT08.S3(NOx);NO2(GT);PT08.S4(NO2);PT08.S5(O3);T;RH;AH\n"
                        "10/03/2004;00.00.00;1.2;2.3;3.4;4.5;5.6;6.7;7.8;8.9;9.0;10.1;11.2;12.3;13.4")

    mocker.patch("app.services.data_service.csv.DictReader", return_value=[
        {"Date": "10/03/2004", "Time": "00.00.00", "CO(GT)": "1.2", "PT08.S1(CO)": "2.3", "NMHC(GT)": "3.4", "C6H6(GT)": "4.5", 
         "PT08.S2(NMHC)": "5.6", "NOx(GT)": "6.7", "PT08.S3(NOx)": "7.8", "NO2(GT)": "8.9", "PT08.S4(NO2)": "9.0", "PT08.S5(O3)": "10.1", 
         "T": "11.2", "RH": "12.3", "AH": "13.4"}
    ])

    # Act
    result = service._process_csv(mock_csv)

    # Assert
    assert result == [{
        "timestamp": datetime(2004, 3, 10), "CO_GT": 1.2, "PT08_S1_CO": 2.3, "NMHC_GT": 3.4, 
        "C6H6_GT": 4.5, "PT08_S2_NMHC": 5.6, "NOx_GT": 6.7, "PT08_S3_NOx": 7.8, 
        "NO2_GT": 8.9, "PT08_S4_NO2": 9.0, "PT08_S5_O3": 10.1, "T": 11.2, "RH": 12.3, "AH": 13.4
    }]

def test_get_all_timestamps(mocker):
    # Arrange
    mock_repository = mocker.patch("app.services.data_service.AirQualityRepository")
    mock_repository_instance = mock_repository.return_value
    mock_repository_instance.get_all_timestamps.return_value = [{"timestamp": "2004-03-10T00:00:00"}]

    service = AirQualityService()  # This will now use the mocked repository

    # Act
    result = service.get_all_timestamps()

    # Assert
    assert result == [{"timestamp": "2004-03-10T00:00:00"}]
