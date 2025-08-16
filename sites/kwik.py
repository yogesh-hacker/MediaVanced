import requests
from bs4 import BeautifulSoup
import json
import re
import ast
from urllib.parse import urlparse

'''
Supports:
https://kwik.si/
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
base_url = "https://kwik.si/e/YPofXhANgdDG"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent
}

# Utility Functions
''' JS Unpacker '''
def unpack(p, a, c, k, e=None, d=None):
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    def base_encode(n):
        rem = n % a
        digit = chr(rem + 29) if rem > 35 else digits[rem]
        if n < a:
            return digit
        return base_encode(n // a) + digit

    d = {} if d is None else d
    for i in range(c - 1, -1, -1):
        key = base_encode(i)
        d[key] = k[i] if i < len(k) and k[i] else key

    pattern = re.compile(r'\b\w+\b')
    def replace(m):
        w = m.group(0)
        return d.get(w, w)

    return pattern.sub(replace, p)

# Fetch initial response
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Sort out correct script
js_code = re.search(r';(eval\(?.*?m3u8.*?\)\))', response).group(1)

# Extract and clean the JS code
encoded_packed = re.sub(r'eval\(function\([^\)]*\)\{.*?}\(|.split.*?\)\)', '', js_code)
data = ast.literal_eval(encoded_packed)

# Extract values from packed data and decode
p,a,c,k,e,d = data[0], int(data[1]), int(data[2]), data[3].split('|'), 0, {}
decoded_data = unpack(p,a,c,k,e,d)

# Get Video URL
video_url = re.search(r"source=\'(.*?)\'", decoded_data).group(1)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")