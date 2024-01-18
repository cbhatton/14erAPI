import requests
import json

from functools import wraps


def retry(retries=3):
    def retry_decorator(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries = retries
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    mtries -= 1
            return "Ran out of retries"

        return f_retry

    return retry_decorator


@retry()
def get_weather(x, y):
    # Making an HTTP GET request to the National Weather Service API and putting the parsed content into a dictionary
    r = requests.get(f'https://api.weather.gov/points/{x},{y}')
    c = json.loads(r.content)

    # Extracting the grid ID, and the X and Y coordinates from the response's properties dictionary
    gridId = c['properties']['gridId']
    gridX = c['properties']['gridX']
    gridY = c['properties']['gridY']

    # Another HTTP GET request to retrieve the detailed forecast information
    response = requests.get(f'https://api.weather.gov/gridpoints/{gridId}/{gridX},{gridY}/forecast')

    if response.status_code is 200:
        content = json.loads(response.content)
    else:
        raise Exception
        return f"there was an error in retrieving the weather: {response.status_code}"

    # finally we return the forcast in a list of periods
    forecast = content['properties']['periods']

    return forecast

