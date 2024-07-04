import requests
from requests import Response
import json
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

url = "https://api.atdata.com"

routes = {
    "safe_to_send": "/v5/ev?",
    "alternate_email": "/ae?",
    "email_append": "/v5/eppend?",
    "postal_append": "/v5/eppend?",
    "demographics": "/v5/td",
    "bulk_demo": "/v5/ei/bulk",
}


def save_response(response: Response, file_name):
    status = response.status_code
    print(status)
    if status == 204:
        return True

    try:
        response_data = response.json()
    except json.JSONDecodeError:
        response_data = {"content": response.content.decode("utf-8")}

    if file_name == "token":
        file_path = f"./code/{file_name}.json"
        with open(file_path, "w") as json_file:
            json.dump(response_data, json_file, indent=4)
        return

    main_path = f"./code/responses/{file_name}"
    os.makedirs(main_path, exist_ok=True)
    file_path = f"{main_path}/{file_name}_{status}.json"

    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            try:
                existing_data = json.load(json_file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                existing_data = []

    if not isinstance(existing_data, list):
        existing_data = []

    existing_data.append(response_data)

    with open(file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)


def read_json(file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_headers():
    return {
        "accept": "application/json",
        "Content-Type": "application/json",
    }


def safeToSend():
    request = "safe_to_send"
    endpoint = f"{url}{routes[request]}"
    headers = create_headers()
    api_key = os.getenv(request.upper())

    data = {"api_key": api_key, "email": "demo@atdata.com"}

    encoded_params = urllib.parse.urlencode(data)
    full_url = f"{endpoint}{encoded_params}"

    response = requests.get(full_url, headers=headers)
    save_response(response, "safe_to_send")


def alternate_email():
    request = "email_append"
    endpoint = f"{url}{routes[request]}"
    headers = create_headers()
    api_key = os.getenv(request.upper())

    data = {"api_key": api_key, "email": "sampleatdata.com"}

    encoded_params = urllib.parse.urlencode(data)
    full_url = f"{endpoint}{encoded_params}"

    response = requests.get(full_url, headers=headers)
    save_response(response, "alternate_email")


def email_append():
    request = "email_append"
    endpoint = f"{url}{routes[request]}"
    headers = create_headers()
    api_key = os.getenv(request.upper())

    data = {
        "api_key": api_key,
        "first": "Joe",
        "last": "Bloggs",
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zip": "38067",
    }

    encoded_params = urllib.parse.urlencode(data)
    full_url = f"{endpoint}{encoded_params}"

    response = requests.get(full_url, headers=headers)
    save_response(response, request)


def postal_append():
    request = "postal_append"
    endpoint = f"{url}{routes[request]}"
    headers = create_headers()
    api_key = os.getenv(request.upper())

    data = {
        "api_key": api_key,
        "email": "postal_sample1@atdata.com",
    }

    encoded_params = urllib.parse.urlencode(data)
    full_url = f"{endpoint}{encoded_params}"

    response = requests.get(full_url, headers=headers)
    save_response(response, request)


if __name__ == "__main__":
    # safeToSend()
    # alternate_email()
    # email_append()
    postal_append()
