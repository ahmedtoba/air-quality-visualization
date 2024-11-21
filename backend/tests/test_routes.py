import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_upload_data(client):
    with open('backend/dataset/air_quality.xlsx', 'rb') as file:
        response = client.post('/api/upload', data={'file': file})
    assert response.status_code == 200
    assert response.json['message'] == "Data successfully ingested!"

def test_get_data(client, mocker):
    mock_data = [{"timestamp": "2023-01-01", "co": 0.5}]
    mocker.patch('app.services.data_service.fetch_data', return_value=mock_data)

    response = client.get('/api/data?parameter=co&start_date=2023-01-01&end_date=2023-01-02')
    assert response.status_code == 200
    assert response.json == mock_data
