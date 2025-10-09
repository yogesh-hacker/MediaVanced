import re
import random
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from urllib.parse import urlparse, quote


'''
Supports:
https://vidrock.net/
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
base_url = "https://vidrock.net/movie/533535/"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))
passphrase = "x7k9mPqT2rWvY8zA5bC3nF6hJ2lK4mN9"
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent,
}

# Extract item ID from base URL
item_type = "tv"
if 'movie' in base_url:
    item_type = "movie"
    item_id = re.search(r'movie\/(\d+)', base_url).group(1)
else:
    match = re.search(r'tv\/(\d+)\/(\d+)\/(\d+)', base_url)
    item_id = f"{match.group(1)}_{match.group(2)}_{match.group(3)}"

# Set up encryption params
key = passphrase.encode()
iv = key[0:16]

# Encrypt and URL encode
cipher = AES.new(key, AES.MODE_CBC, iv)
ct = cipher.encrypt(pad(item_id.encode(), AES.block_size))
encoded = quote(base64.b64encode(ct).decode())

# Get streaming info
response = requests.get(f'{default_domain}/api/{item_type}/{encoded}').json()

# Load all valid sources
sources = []
for src in response.values():
    if src.get('url'):
        sources.append(src['url'])

# Pick a random video URL
video_url = random.choice(sources)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")