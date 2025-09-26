import re
import json
import time
import base64
import requests
from urllib.parse import urlparse, quote

'''
Supports:
https://mapple.tv/
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
base_url = "https://mapple.tv/watch/tv/2-1/110316-alice-in-borderland"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
key = "nanananananananananananaBatman!"
default_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent
}

# Utility Functions
'''XOR Data Encryptor'''
def encrypt_data(url: str) -> str:
    payload = json.dumps({"url": url, "timestamp": int(time.time() * 1000)}, separators=(',', ':'))
    encoded = quote(payload)

    key_len = len(key)
    xored_bytes = bytes(
        ord(ch) ^ ord(key[i % key_len]) for i, ch in enumerate(encoded)
    )
    
    return base64.urlsafe_b64encode(xored_bytes).decode().rstrip('=')

# Build the request payload
data = {}
if "movie" in base_url:
    media_id = int(base_url.rsplit('/', 1)[-1].split('-')[0])
    data.update({
        'mediaId': media_id,
        'mediaType': 'movie',
        'source': 'mapple',
        'tv_slug': ''
    })
else:
    match = re.search(r'/tv/(\d+)-(\d+)/(\d+)', base_url)
    season, episode, media_id = map(int, match.groups())
    data.update({
        'mediaId':media_id,
        'mediaType': 'tv',
        'source': 'mapple',
        'tv_slug': f'{season}-{episode}',
    })

# Encrypt the payload and prepare the API URL
encrypted_data = encrypt_data(json.dumps(data, separators=(',', ':')))
api_url = f'{default_domain}/api/stream-encrypted?data={encrypted_data}'

# Fetch streaming data from the API
response = requests.get(api_url, headers=headers).json()
if response.get('success') == False:
    exit(f"ERROR: {response.get('error')}")

# Extract video URL
video_url = response.get('data').get('stream_url')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")