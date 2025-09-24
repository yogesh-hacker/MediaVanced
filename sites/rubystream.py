import re
import ast
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

'''
Supports:
https://rubystm.com/
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
base_url = "https://rubystm.com/e/6kt64xxjjlks.html"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent,
}

# Utility Functions
''' Base-36 conversion helper function '''
def to_base_36(n):
    return '' if n == 0 else to_base_36(n // 36) + "0123456789abcdefghijklmnopqrstuvwxyz"[n % 36]

''' Replace placeholders with corresponding values '''
def unpack(p,a,c,k,e,d):
    for i in range(c):
        if k[c - i - 1]:
            p = re.sub(r'\b' + to_base_36(c - i - 1) + r'\b', k[c - i - 1], p)
    return p

# Get intial page
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, "html.parser")

# Extract form data
data = {}
form = soup.find("form", {"id": "F1"})
for input_tag in form.find_all("input"):
    name = input_tag.get("name")
    value = input_tag.get("value", "")
    data[name] = value

data["file_code"] = base_url.split('/')[-1].replace('.html', '')
data["referer"] = default_domain

# Submit form to get streaming page
response = requests.post(f'{default_domain}/dl', headers=headers, data=data).text

# Packed data pattern
pattern = r'eval\(function\((.*?)\)\{.*\}\((.*?\))\)\)'
data_match = re.search(pattern, response)

# Extract packed data if found
data = None
if data_match:
    data = data_match.group(2).replace(".split('|')", "");
    data = ast.literal_eval(data)
else:
    print("Failed to extract packed data.")

# Extract variables from packed data
p,a,c,k,e,d = data[0], int(data[1]), int(data[2]), data[3].split('|'), None, None

# Replace function to decode the packed data
decoded_data = unpack(p,a,c,k,e,d)

# Extract video URL
video_url = re.search(r'file:\"(.*?)\"', decoded_data).group(1)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")