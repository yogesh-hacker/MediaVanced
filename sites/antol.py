import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import re
import json 
import json

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
    

base_url = "https://antol307vvk.com/play/tt26548265"
default_domain = "https://antol307vvk.com"
initial_headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}
print(f"\n{Colors.OKCYAN}TARGET: {default_domain}{Colors.ENDC}")
print(f"{Colors.BOLD}I dont know this website og name if you know please send me message{Colors.ENDC}\n")

cookies = {
    'user_id': '3316641453',
    'sku': '01J28X81T07BA9D023VY5JQRJAD_gamechanger_cue_piece'
}

proxy = {
    "http": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128",
    "https": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128"
}

session = requests.Session()
session.proxies.update(proxy)

initial_response = session.get(base_url, headers=initial_headers)
response_text = initial_response.text
match = re.search(r'"file":"([^"]+)"', response_text)
url = match.group(1)
url = url.replace('\\/', '/')
match = re.search(r'"key":"([^"]+)"', response_text)
key = match.group(1)
key = key.replace('\\/', '/')
initial_headers['X-CSRF-TOKEN'] = key
base_url = default_domain+url 
initial_response = session.post(base_url, headers=initial_headers)
data = json.loads(initial_response.text)
hindi_file = next((item['file'] for item in data if item['title'] == 'Hindi'), None)
cleaned_file = hindi_file.replace('~', '')
base_url = f'{default_domain}/playlist/{cleaned_file}.txt'
initial_response = session.post(base_url, headers=initial_headers)
initial_response = session.post(initial_response.text, headers=initial_headers)
full_url = initial_response.url
base_url = full_url.rsplit('/', 1)[0]
lines = initial_response.text.splitlines()
quality_paths = []

for line in lines:
    if line.startswith('#EXT-X-STREAM-INF'):
        index = lines.index(line) + 1
        if index < len(lines):
            path = lines[index]
            if path.startswith('./'):
                path = path[2:]
            quality_paths.append(path)

for path in quality_paths:
    print(f"\nCaptured URL: {Colors.OKGREEN}{base_url}/{path}{Colors.ENDC}\n")