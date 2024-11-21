from app.services.data_service import ingest_data, fetch_data
from unittest.mock import MagicMock
import pandas as pd

def test_ingest_data(mocker):
    mock_mongo = mocker.patch('app.mongo.db.air_quality.insert_many')
    file = MagicMock()
    df = pd.DataFrame({"timestamp": ["2023-01-01"], "co": [0.5]})
    mocker.patch('pandas.read_excel', return_value=df)

    result = ingest_data(file)
    mock_mongo.assert_called_once()
    assert result == "Data successfully ingested!"

def test_fetch_data(mocker):
    mock_mongo = mocker.patch('app.mongo.db.air_quality.find', return_value=[{"co": 0.5}])
    data = fetch_data("co", "2023-01-01", "2023-01-02")
    mock_mongo.assert_called_once()
    assert data == [{"co": 0.5}]
