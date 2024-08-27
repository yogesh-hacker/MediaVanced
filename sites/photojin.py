import requests
from bs4 import BeautifulSoup
import json

session = requests.Session()
initial_url = "https://photojin.lol/download/jBNOL-RbNxM"

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

initial_response = session.get(initial_url)

if initial_response.status_code == 200:
    #redirected_response = session.get(initial_response)
    soup = BeautifulSoup(initial_response.text, 'html.parser')
    data_field = soup.find("section", id="generate_url")
    

    data = {
        "type": "DOWNLOAD_GENERATE",
        "payload": {
            "uid": data_field['data-uid'],
            "access_token": data_field['data-token']
        }
    }
    json_data = json.dumps(data)

    headers = {"X-Requested-With": "xmlhttprequest"}
    post_response = session.post("https://photojin.online/action", data=json_data, headers=headers)

    captured_url = post_response.json()['download_url']
    print("\n######################")
    print("######################")
    print(f"Captured URL: {Colors.OKGREEN}{captured_url}{Colors.ENDC}")
    print("######################")
    print("######################\n")
else:
    print("\n######################")
    print("######################")
    print(f"ERROR: Expected 200 or 302, got {initial_response.status_code}.")
    print("######################")
    print("######################\n")

