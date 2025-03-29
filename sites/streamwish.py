import requests
from bs4 import BeautifulSoup
import json
import re
import ast
from urllib.parse import urlparse

'''
Supports:
https://streamwish.to/
https://rapidplayers.com/
https://moflix-stream.click/
https://dhtpre.com/
https://vidhide.com/
https://mixdrop.ps/
https://multimovies.cloud/
https://hlsflex.com/
https://ghbrisk.com/
https://niikaplayerr.com/
https://uqloads.xyz/
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

base_url = "https://uqloads.xyz/e/93em7lspo9lo"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
headers = {
    'Referer': 'https://player4u.xyz/',
    'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
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

# Fetch response
response = requests.get(base_url, headers=headers).text

# Fetch and parse the initial response
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

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")
