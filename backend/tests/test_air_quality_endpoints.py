import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


def test_get_by_date_range(client, mocker):
    mocker.patch("app.services.data_service.AirQualityService.get_by_date_range", return_value=[
        {"timestamp": "2004-03-10T00:00:00", "CO_GT": 1.2}
    ])
    
    response = client.get("/air-quality?start_date=10-03-2004&end_date=20-03-2004")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["CO_GT"] == 1.2


def test_bulk_ingest_csv(client, mocker):
    mocker.patch("app.services.data_service.AirQualityService.bulk_ingest_csv", return_value="1 rows successfully ingested.")
    
    data = {"file": (open("tests/test_data.csv", "rb"), "test_data.csv")}
    response = client.post("/air-quality/ingest_data", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert "1 rows successfully ingested" in response.json["message"]
