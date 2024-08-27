import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import re
import json 
import cfscrape
import json
import base64

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

def save_file_in_internal_directory(filename, content, directory='/storage/emulated/0'):
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
    

base_url = "https://vcloud.lol/pwgzyiui3buxr1w"
default_domain = "https://vcloud.lol/"
initial_headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}
print(f"\n{Colors.OKCYAN}TARGET: {default_domain}{Colors.ENDC}")

cookies = {
    'user_id': '3316641453',
    'sku': '01J28X81T07BA9D023VY5JQRJAD_gamechanger_cue_piece'
}

proxy = {
    "http": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128",
    "https": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128"
}

data = {

}

session = requests.Session()
#session.proxies.update(proxy)

initial_response = session.post(base_url, headers=initial_headers)
response_text = initial_response.text

match = re.search(r"var\s+url\s*=\s*'(https?:\/\/[^\s]+)'", response_text)
base_url = match.group(1)

initial_response = session.get(base_url, headers=initial_headers)
response_text = initial_response.text
match = re.search(r"var\s+url\s*=\s*'(https?:\/\/[^\s]+)'", response_text)

download_url = match.group(1)
print("######################")
print("######################")
print(f"Captured URL: {Colors.OKGREEN}{download_url}{Colors.ENDC}")
print("######################")
print("######################\n")