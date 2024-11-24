import pytest
from datetime import datetime
from unittest.mock import MagicMock
from app.repositories.air_quality_repository import AirQualityRepository


@pytest.fixture
def mock_db(mocker):
    mock_collection = MagicMock()
    mocker.patch("app.repositories.air_quality_repository.get_database", return_value={"air_quality_data": mock_collection})
    return mock_collection


def test_find_by_date_range(mock_db):
    repository = AirQualityRepository()
    mock_db.find.return_value = [{"timestamp": datetime(2004, 3, 10), "CO_GT": 1.2}]
    
    start_date = datetime(2004, 3, 10)
    end_date = datetime(2004, 3, 20)
    result = list(repository.find_by_date_range(start_date, end_date))
    
    mock_db.find.assert_called_once_with(
        {"timestamp": {"$gte": datetime(2004, 3, 10, 0, 0), "$lte": datetime(2004, 3, 20, 23, 59, 59)}}
    )
    assert len(result) == 1
    assert result[0]["CO_GT"] == 1.2


def test_bulk_insert(mock_db):
    repository = AirQualityRepository()
    data = [{"timestamp": datetime(2004, 3, 10), "CO_GT": 1.2}]
    
    repository.bulk_insert(data)
    mock_db.insert_many.assert_called_once_with(data)


def test_get_all_timestamps(mock_db):
    repository = AirQualityRepository()
    mock_db.find.return_value = [{"timestamp": datetime(2004, 3, 10)}]
    
    result = list(repository.get_all_timestamps())
    mock_db.find.assert_called_once_with({}, {"timestamp": 1})
    assert len(result) == 1
    assert result[0]["timestamp"] == datetime(2004, 3, 10)
