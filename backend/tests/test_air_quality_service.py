import pytest
from datetime import datetime
from unittest.mock import MagicMock
from app.services.data_service import AirQualityService


@pytest.fixture
def mock_repository(mocker):
    return mocker.patch("app.services.data_service.AirQualityRepository")


def test_get_by_date_range(mock_repository):
    service = AirQualityService()
    mock_repository.return_value.find_by_date_range.return_value = [
        {"timestamp": datetime(2004, 3, 10), "CO_GT": 1.2}
    ]
    
    start_date = datetime(2004, 3, 10)
    end_date = datetime(2004, 3, 20)
    result = service.get_by_date_range(start_date, end_date)
    
    mock_repository.return_value.find_by_date_range.assert_called_once_with(start_date, end_date)
    assert len(result) == 1
    assert result[0]["CO_GT"] == 1.2


def test_bulk_ingest_csv(mock_repository, mocker):
    service = AirQualityService()
    mock_repository.return_value.get_all_timestamps.return_value = [{"timestamp": datetime(2004, 3, 10)}]
    mock_repository.return_value.bulk_insert = MagicMock()
    
    csv_file = mocker.Mock()
    mocker.patch("csv.DictReader", return_value=[
        {"Date": "11/03/2004", "Time": "00.00.00", "CO(GT)": "1.2", "T": "11.3", "RH": "56.8", "AH": "0.76"}
    ])
    
    result = service.bulk_ingest_csv(csv_file)
    assert "1 rows successfully ingested" in result
    mock_repository.return_value.bulk_insert.assert_called_once()


def test_add_one(mock_repository):
    service = AirQualityService()
    mock_repository.return_value.find_by_timestamp.return_value = None
    
    air_quality_data = {"timestamp": datetime(2004, 3, 10), "CO_GT": 1.2}
    service.add_one(air_quality_data)
    
    mock_repository.return_value.insert_one.assert_called_once_with(air_quality_data)
