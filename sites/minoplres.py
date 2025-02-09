from requests import get, post
from bs4 import BeautifulSoup
import re
import os

'''
Supports:
https://minoplres.xyz/
https://embdproxy.xyz/
'''

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

default_domain = "https://embdproxy.xyz/"
base_url = "https://embdproxy.xyz/embed-xgk3dxfa15oo.html"
initial_headers = {
    'Referer': default_domain
}

initial_response = get(base_url, headers = initial_headers)
initial_page_html = initial_response.text
pattern = r'file:"([^"]+)"'
match = re.search(pattern, initial_page_html)
if match:
    video_url = match.group(1)
    print("\n" + "#"*25 + "\n" + "#"*25)
    print(f"Captured URL: {Colors.OKGREEN}{video_url}{Colors.ENDC}")
    print("#"*25 + "\n" + "#"*25)
    print(f"{Colors.WARNING}###Please use header Referer: https://embdproxy.xyz/ or host of the CDN to access the url\n")
    
else:
    print("URL not found.")
