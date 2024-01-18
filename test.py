import requests
import json

BASE_URL = "http://127.0.0.1:5000" # or wherever your app is running

def test_get_peaks():
    response = requests.get(f"{BASE_URL}/peaks")
    print(response)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

test_get_peaks()