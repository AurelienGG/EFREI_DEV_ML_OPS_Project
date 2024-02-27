import requests

# Base URL of the API
BASE_URL = "http://localhost:8000"


def test_predict_endpoint_returns_200():
    response = requests.post(f"{BASE_URL}/predict/", files={'file': open('pikachu.png', 'rb')})
    assert response.status_code == 200


def test_predict_endpoint_returns_json():
    response = requests.post(f"{BASE_URL}/predict/", files={'file': open('pikachu.png', 'rb')})
    assert response.headers['Content-Type'] == 'application/json'


def test_predict_endpoint_structure():
    response = requests.post(f"{BASE_URL}/predict/", files={'file': open('pikachu.png', 'rb')})
    data = response.json()
    assert 'predicted_name' in data
    assert 'class_probabilities' in data
    assert isinstance(data['class_probabilities'], list)

# Add more tests as needed
