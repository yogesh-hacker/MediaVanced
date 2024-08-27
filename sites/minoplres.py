from requests import get, post
from bs4 import BeautifulSoup
import re
import os

default_domain = "https://minoplres.xyz/"
base_url = "https://minoplres.xyz/embed-xgk3dxfa15oo.html"
initial_headers = {
    'Referer': default_domain
}

def save_file_in_internal_directory(filename, content, directory='/storage/emulated/0'):
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

proxy = {
    "http": "http://qvgxntjn:1cyxq9jfd6rh@45.94.47.66:8110",
    "https": "http://qvgxntjn:1cyxq9jfd6rh@45.94.47.66:8110"
}

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

print(f"\n{Colors.OKCYAN}TARGET: {default_domain}{Colors.ENDC}")

initial_response = get(base_url, headers = initial_headers)
initial_page_html = initial_response.text
pattern = r'file:"([^"]+)"'
match = re.search(pattern, initial_page_html)
save_file_in_internal_directory("minoplres.html", initial_page_html)
if match:
    stream_url = match.group(1)
    print("######################")
    print("######################")
    print(f"Captured URL: {Colors.OKGREEN}{stream_url}{Colors.ENDC}")
    print("######################")
    print("######################")
    print(f"{Colors.WARNING}###Please use header Referer: https://minoplres.xyz/ or host of the CDN to access the url\n")
    
else:
    print("URL not found.")
