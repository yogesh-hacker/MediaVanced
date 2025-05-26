import re
import json
import codecs
import requests
from base64 import b64decode
from bs4 import BeautifulSoup
from urllib.parse import urlparse

'''
Supports:
https://voe.sx/
https://kellywhatcould.com/
https://jilliandescribecompany.com/
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
base_url = "https://jilliandescribecompany.com/e/ueof3kkmzcal"
user_agent = "Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent
}

# Utility Functions
''' Replaces custom symbol patterns with underscores'''
def clean_symbols(s):
    for p in ["@$", "^^", "~@", "%?", "*~", "!!", "#&"]:
        s = re.sub(re.escape(p), "_", s)
    return s

''' Removes all underscores from the string'''
def clean_underscores(s):
    return s.replace("_", "")

''' Shifts each character back by a given number '''
def shift_back(s, n):
    return ''.join(chr(ord(c) - n) for c in s)

# Fetch initial page
response = requests.get(base_url, headers=headers).text
if 'Redirecting...' in response:
    base_url = re.search(r"href\s*=\s*'(.*?)';", response).group(1)
    response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Get obfuscated data
obfuscated_script = soup.find('script', attrs={'type': 'application/json'}).string
encoded_data = re.search(r'\["(.*?)"\]', obfuscated_script).group(1)

# Start decoding process
decoded_data = codecs.decode(encoded_data, 'rot_13')
decoded_data = clean_symbols(decoded_data)
decoded_data = clean_underscores(decoded_data)
decoded_data = b64decode(decoded_data).decode()
decoded_data = shift_back(decoded_data, 3)
decoded_data = decoded_data[::-1] # Reverse
decoded_data = b64decode(decoded_data).decode()
decoded_data = json.loads(decoded_data)

# Extract video URL
video_url = decoded_data['source']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")