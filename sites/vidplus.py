import re
import json
import random
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from urllib.parse import urlparse
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2


'''
Supports:
https://player.vidplus.to/
https://vidplus.to/
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
base_url = "https://player.vidplus.to/embed/movie/587412?server=1"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))
headers = {
    "Accept": "*/*",
    "Referer": default_domain,
    "User-Agent": user_agent,
    "X-Requested-With": "XMLHttpRequest"
}

# Get server and ID
item_id = re.search(r'\/(?:movie|webseries)\/(\d+)', base_url).group(1)
server = 4 # Default server (Try changing the number if scraper fails)

# Get Movie/Webseries info
data = {
    "id": item_id,
    "key": "cGxheWVyLnZpZHNyYy5jb19zZWNyZXRLZXk="
}
encoded = base64.b64encode(json.dumps(data).encode()).decode()
api_url = f'{default_domain}/api/tmdb?params=cbc7.{encoded}.9lu'
response = requests.get(api_url, headers=headers).json()

# Get required data
metadata = response.get('data')
imdb_id = metadata.get('imdb_id')
title = metadata.get('title')
release_year = metadata.get('release_date').split('-')[0]

# Build request parameters and fetch encrypted response
request_args = '*'.join([title, release_year, imdb_id])
response = requests.get(f'{default_domain}/api/server?id={item_id}&sr={server}&args={request_args}', headers=headers).json()

# Decode the base64-encoded JSON container
encoded_payload = response.get('data')
decoded_payload = base64.b64decode(encoded_payload).decode('utf-8')
payload_json = json.loads(decoded_payload)

# Extract encryption parameters
ciphertext = base64.b64decode(payload_json.get('encryptedData'))
password = payload_json.get('key')
salt = bytes.fromhex(payload_json.get('salt'))
iv = bytes.fromhex(payload_json.get('iv'))

# Derive AES decryption key using PBKDF2 (SHA256)
derived_key = PBKDF2(password, salt, dkLen=32, count=1000, hmac_hash_module=SHA256)

# Initialize AES cipher and decrypt
cipher = AES.new(derived_key, AES.MODE_CBC, iv)
decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

# Parse final JSON containing streaming details
streaming_info = json.loads(decrypted_text)

# Resolve proxied URL to actual stream URL
proxy_url = f"{default_domain}{streaming_info.get('url')}"
response = requests.head(proxy_url, headers=headers).headers
video_url = response['Location']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Origin:{Colors.endc} {default_domain}")
print("\n")
