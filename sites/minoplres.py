from requests import get, post
from bs4 import BeautifulSoup
import re

default_domain = "https://minoplres.xyz/"
base_url = "https://minoplres.xyz/embed-l1s6pevitg6y.html"
initial_headers = {
    'Referer': default_domain
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
