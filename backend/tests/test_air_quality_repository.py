from app.repositories.air_quality_repository import AirQualityRepository
from app.db_connection import get_database
from datetime import datetime
from unittest.mock import MagicMock, patch

def test_find_by_parameter(mocker):
    # Arrange
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mocker.patch("app.repositories.air_quality_repository.get_database").return_value = mock_db
    repository = AirQualityRepository()
    mock_collection.find.return_value = [{"timestamp": "2004-03-10T00:00:00", "CO_GT": 1.2}]

    # Act
    result = repository.find_by_parameter("CO_GT", datetime(2004, 3, 10), datetime(2004, 3, 20))

    # Assert
    assert result == [{"timestamp": "2004-03-10T00:00:00", "CO_GT": 1.2}]

def test_find_by_date_range(mocker):
    # Arrange
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mocker.patch("app.repositories.air_quality_repository.get_database").return_value = mock_db
    repository = AirQualityRepository()
    mock_collection.find.return_value = [{
        "timestamp": "2004-03-10T00:00:00", "CO_GT": 1.2, "PT08_S1_CO": 2.3, 
        "NMHC_GT": 3.4, "C6H6_GT": 4.5, "PT08_S2_NMHC": 5.6, "NOx_GT": 6.7, 
        "PT08_S3_NOx": 7.8, "NO2_GT": 8.9, "PT08_S4_NO2": 9.0, "PT08_S5_O3": 10.1, 
        "T": 11.2, "RH": 12.3, "AH": 13.4
    }]

    # Act
    result = repository.find_by_date_range(datetime(2004, 3, 10), datetime(2004, 3, 20))

    # Assert
    assert result == [{
        "timestamp": "2004-03-10T00:00:00", "CO_GT": 1.2, "PT08_S1_CO": 2.3, 
        "NMHC_GT": 3.4, "C6H6_GT": 4.5, "PT08_S2_NMHC": 5.6, "NOx_GT": 6.7, 
        "PT08_S3_NOx": 7.8, "NO2_GT": 8.9, "PT08_S4_NO2": 9.0, "PT08_S5_O3": 10.1, 
        "T": 11.2, "RH": 12.3, "AH": 13.4
    }]

def test_bulk_insert(mocker):
    # Arrange
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mocker.patch("app.repositories.air_quality_repository.get_database").return_value = mock_db
    repository = AirQualityRepository()
    mock_collection.insert_many.return_value = None

    # Act
    repository.bulk_insert([{
        "timestamp": "2004-03-10T00:00:00", "CO_GT": 1.2, "PT08_S1_CO": 2.3, 
        "NMHC_GT": 3.4, "C6H6_GT": 4.5, "PT08_S2_NMHC": 5.6, "NOx_GT": 6.7, 
        "PT08_S3_NOx": 7.8, "NO2_GT": 8.9, "PT08_S4_NO2": 9.0, "PT08_S5_O3": 10.1, 
        "T": 11.2, "RH": 12.3, "AH": 13.4
    }])

    # Assert
    mock_collection.insert_many.assert_called_once_with([{
        "timestamp": "2004-03-10T00:00:00", "CO_GT": 1.2, "PT08_S1_CO": 2.3, 
        "NMHC_GT": 3.4, "C6H6_GT": 4.5, "PT08_S2_NMHC": 5.6, "NOx_GT": 6.7, 
        "PT08_S3_NOx": 7.8, "NO2_GT": 8.9, "PT08_S4_NO2": 9.0, "PT08_S5_O3": 10.1, 
        "T": 11.2, "RH": 12.3, "AH": 13.4
    }])

def test_get_all_timestamps(mocker):
    # Arrange
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mocker.patch("app.repositories.air_quality_repository.get_database").return_value = mock_db
    repository = AirQualityRepository()
    mock_collection.find.return_value = [{"timestamp": "2004-03-10T00:00:00"}]

    # Act
    result = repository.get_all_timestamps()

    # Assert
    assert result == [{"timestamp": "2004-03-10T00:00:00"}]
