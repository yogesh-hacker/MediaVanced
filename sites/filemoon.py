import requests
from bs4 import BeautifulSoup
import json
import re
import ast
from urllib.parse import urlparse

'''
Supports:
https://filemoon.to/
https://2glho.org/
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
base_url = "https://filemoon.to/e/b0ypyzt8ewqo"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": default_domain,
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "Sec-Fetch-Dest": "iframe",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": user_agent
}

# Utility Functions
# Base-36 conversion helper function
def to_base_36(n):
    return '' if n == 0 else to_base_36(n // 36) + "0123456789abcdefghijklmnopqrstuvwxyz"[n % 36]

# Replace placeholders with corresponding values
def unpack(p,a,c,k,e,d):
    for i in range(c):
        if k[c - i - 1]:
            p = re.sub(r'\b' + to_base_36(c - i - 1) + r'\b', k[c - i - 1], p)
    return p

# Fetch initial response
response = requests.get(base_url, headers=headers).text

# Fetch and parse the iframe URL
soup = BeautifulSoup(response, 'html.parser')
iframe_url = soup.select_one('iframe')['src']

# Get iframe content and procced for extraction
response = requests.get(iframe_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

js_code = next((script.string for script in soup.find_all('script') if script.string and "eval(function(p,a,c,k,e,d)" in script.string), "")

# Extract and clean the JS code
encoded_packed = re.sub(r"eval\(function\([^\)]*\)\{[^\}]*\}\(|.split\('\|'\)\)\)", '', js_code)
data = ast.literal_eval(encoded_packed)

# Extract values from packed data and decode
p,a,c,k,e,d = data[0], int(data[1]), int(data[2]), data[3].split('|'), None, None

decoded_data = unpack(p,a,c,k,e,d)

# Get Video URL
video_url = re.search(r'file:"([^"]+)', decoded_data).group(1)

# Print Results
print("\n" + "#"*25 + "\n" + "#"*25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#"*25 + "\n" + "#"*25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print(f"{Colors.okcyan}User-Agent:{Colors.endc} {user_agent}")
print("\n")