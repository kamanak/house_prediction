import requests
import json
url = 'http://127.0.0.1:8000/predict'

headers = {
    'accept':'application/json',
    'Content-Type': 'application/json'

}
params = {
  "MedInc": 8.3252,
  "HouseAge": 41.0,
  "AveRooms": 6.984127,
  "AveBedrms": 1.023810,
  "Population": 322.0,
  "AveOccup": 2.555556,
  "Latitude": 37.88,
  "Longitude": -122.23
}
# response = requests.post(url,headers=headers,params=params)
response = requests.post(url,headers=headers,data=json.dumps(params))
try:
    response.raise_for_status()  # Check for HTTP errors
    result = response.json()
    print(result)
except json.JSONDecodeError:
    print("Failed to decode JSON response. Response might be empty or not in JSON format.")
except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.RequestException as err:
    print(f"Request Error: {err}")
