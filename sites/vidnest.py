import re
import json
import random
import base64
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse

'''
Supports:
https://vidnest.fun/
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
base_url = 'https://vidnest.fun/tv/94605/1/1'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
passphrase = 'T8c8PQlSQVU4mBuW4CbE/g57VBbM5009QHd+ym93aZZ5pEeVpToY6OdpYPvRMVYp'
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Pick a random server and get ID
servers = ['allmovies', 'hollymoviehd']
server = random.choice(servers)

# Get item id
media_type = 'movie'
if 'tv' in base_url:
    media_type = 'tv'
    item_id = base_url.split('/tv/')[-1]
else:
    item_id = base_url.split('/movie/')[-1]

# Fetch encrypted streams
response = requests.get(f'https://backend.vidnest.fun/{server}/{media_type}/{item_id}', headers=headers).json()
b64_encoded = response.get('data')

# Prepare decryption params
encrypted_bytes = base64.b64decode(b64_encoded)
key = base64.b64decode(passphrase)[:32]
iv = encrypted_bytes[:12]
ciphertext = encrypted_bytes[12:-16]
tag = encrypted_bytes[-16:]

# Decrypt encrypted data (AES-GCM)
cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
plaintext = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')

# Parse decrypted JSON and validate server response
json_data = json.loads(plaintext)
if not json_data.get('success') and not json_data.get('streams'):
    exit(f'{Colors.fail}ERROR: {json_data.get('error')}\nPlease retry with different server...{Colors.endc}')
sources = json_data.get('sources') or json_data.get('streams')

# Extract video URL
video_url = sources[0].get('file') or sources[0].get('url')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")