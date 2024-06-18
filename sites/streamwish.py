import requests
from bs4 import BeautifulSoup
import json
import re

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
print(f"\n{Colors.OKCYAN}TARGET: streamwish.to{Colors.ENDC}")

default_domain = "https://streamwish.to"
initial_headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

base_url = "https://streamwish.to/balway8gy6b0"
initial_response = requests.get(base_url,headers=initial_headers);
initial_regex = r'file:"([^"]+)"'
initial_match = re.search(initial_regex, initial_response.text)
if initial_match:
    streaming_url = initial_match.group(1)
    print("######################")
    print("######################")
    print(f"Captured URL: {Colors.OKGREEN}{streaming_url}{Colors.ENDC}")
    print("######################")
    print("######################\n")
    print(f"\n{Colors.WARNING}###Please use make sure you have User-Agent in your requests!!!{Colors.ENDC}")
else:
    print(f"{Colors.FAIL}ERROR: Unable to locate streaming url")