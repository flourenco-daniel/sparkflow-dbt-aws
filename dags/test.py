import requests

    # Replace with the actual API endpoint you want to check
api_url = "http://api.openweathermap.org/geo/1.0/direct?limit=5&appid=7ef420e549fa10b892aa2ec65544968e" 

try:
    response = requests.get(api_url)

    # Check the status code
    if response.status_code == 200:
        print(f"API is operational. Status Code: {response.status_code}")
        # You can also access other response data like JSON content
        # data = response.json()
        # print(data)
    elif response.status_code == 404:
        print(f"API endpoint not found. Status Code: {response.status_code}")
    elif response.status_code >= 400 and response.status_code < 500:
        print(f"Client error encountered. Status Code: {response.status_code}")
    elif response.status_code >= 500:
        print(f"Server error encountered. Status Code: {response.status_code}")
    else:
        print(f"Unexpected status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while connecting to the API: {e}")