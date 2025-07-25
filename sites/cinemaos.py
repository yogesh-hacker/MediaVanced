import re
import json
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import unpad

'''
Supports:
https://cinemaos.live/
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
base_url = "https://cinemaos.live/movie/watch/1061474"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
headers = {
    "Accept": "*/*",
    "Referer": default_domain,
    "User-Agent": user_agent,
}

# Get auth token
auth_api = f'{default_domain}/api/auth'
response = requests.get(auth_api, headers=headers).json()
auth_token = requests.post(auth_api, headers=headers, json=response).json()['token']
headers['Authorization'] = f'Bearer {auth_token}'

# Get required data
if 'movie' in base_url:
    data_id = base_url.split('/')[-1]
    response = requests.get(f"{default_domain}/api/downloadLinks?type=movie&tmdbId={data_id}").json()['data'][0]
    release_year = response['releaseYear']
    title = response['movieTitle']
    imdb_id = response['subtitleLink'].split('=')[-1]
else:
    exit(print(f'{Colors.fail}TV Series currently not supported!'))

# Get encrypted data
response = requests.get(f"https://cinemaos.live/api/cinemaos?type=movie&tmdbId={data_id}&imdbId={imdb_id}&t={title}&ry={release_year}", headers=headers).json()['data']

# Extract hex strings from the response
encrypted_hex = response['encrypted']
iv_hex = response['cin']
auth_tag_hex = response['mao']

# Convert Hex to Bytes
key_hex = "6f8c2e9a4b1d7f3e8c5a2b6d9e0f4c1a7b3e5d8c0a2f6b4d9e1c3a7f5b2d8c6e"
key = bytes.fromhex(key_hex)
ciphertext = bytes.fromhex(encrypted_hex)
iv = bytes.fromhex(iv_hex)
auth_tag = bytes.fromhex(auth_tag_hex)

# Decrypt using AES-256-GCM
cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
cipher.update(b'') # AAD
cipher.digest_size = 16
decrypted_data = cipher.decrypt(ciphertext).decode('utf-8')
cipher.verify(auth_tag)

# Extract video URL
json_data = json.loads(decrypted_data)['sources']
valid_entries = [v for v in json_data.values() if isinstance(v, dict) and 'url' in v]
random_choice = random.choice(valid_entries)
video_url = random_choice['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print('\n')