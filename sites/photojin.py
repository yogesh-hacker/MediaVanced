import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse

'''
Supports:
https://photojin.cyou/
'''

class Colors:
    header = '\033[95m'
    okblue = '\033[94m'
    okcyan = '\033[96m'
    okgreen = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'

# Constants
base_url = "https://photojin.cyou/download/Bf5Rg02SnNM"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
headers = {
    "Referer": "https://photojin.sbs/",
    "User-Agent": user_agent
}


# Fetch response
session = requests.Session()
initial_response = session.get(base_url, headers=headers)

# Get latest domain
parsed_url = urlparse(initial_response.url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

# Fetch page HTML
soup = BeautifulSoup(initial_response.text, 'html.parser')
data_field = soup.find("section", id="generate_url")

# Set up post data and headers
data = {
    "type": "DOWNLOAD_GENERATE",
    "payload": {
        "uid": data_field['data-uid'],
        "access_token": data_field['data-token']
    }
}

json_data = json.dumps(data)
headers["X-Requested-With"] = "xmlhttprequest"

# Extract video URL
initial_response = session.post(f"{default_domain}/action", data=json_data, headers=headers)
video_url = initial_response.json()['download_url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
