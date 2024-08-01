import pytest
from web_framework import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

#def test_index(client):
#    """Test the index route"""
#    rv = client.get('/')
#    assert rv.status_code == 200
#    assert b"Welcome to the Weather Data API!" in rv.data

def test_weather_endpoint(client):
    """Test the weather endpoint"""
    rv = client.get('/api/weather?date=19850101&station_id=USC00257715&limit=10&offset=0')
    assert rv.status_code == 200
    # Add more assertions based on the expected response

def test_weather_stats_endpoint_with_params(client):
    """Test the weather endpoint with query parameters"""
    rv = client.get('/api/weather/stats?year=1985&station_id=USC0033&limit=10&offset=0')
    assert rv.status_code == 200
    # Add more assertions based on the expected response