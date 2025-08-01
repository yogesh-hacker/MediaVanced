import re
import json
import base64
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote_plus


'''
Supports:
https://videostr.net/
'''

# @Megacloud, @VideoStr || Love you guys! ❤️

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
provider_url = 'https://flixhq.tube/ajax/episode/sources/11998768'
base_url = requests.get(provider_url).json()['link'] # https://videostr.net/embed-1/v3/e-1/<VIDEO_ID>?z=
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
decode_url = "https://script.google.com/macros/s/AKfycbxHbYHbrGMXYD2-bC-C43D3njIbU-wGiYQuJL61H4vyy6YVXkybMNNEPJNPPuZrD1gRVA/exec"
key_url = "https://raw.githubusercontent.com/yogesh-hacker/MegacloudKeys/refs/heads/main/keys.json"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
headers = {
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": default_domain,
    "User-Agent": user_agent
}

# Fetch initial response
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Get file ID and nonce
video_tag = soup.select_one('#megacloud-player')
if not video_tag:
    exit(print(f'{Colors.fail}Looks like URL expired!{Colors.endc}'))
file_id = video_tag['data-id']

# Get Nonce
match = re.search(r'\b[a-zA-Z0-9]{48}\b', response) or re.search(r'\b([a-zA-Z0-9]{16})\b.*?\b([a-zA-Z0-9]{16})\b.*?\b([a-zA-Z0-9]{16})\b', response)
nonce = ''.join(match.groups()) if match and match.lastindex == 3 else match.group() if match else None

# Get Passphrase 
response = requests.get(key_url).json()
key = response['vidstr']

# Get encrypted data
response = requests.get(f'{default_domain}/embed-1/v3/e-1/getSources?id={file_id}&_k={nonce}', headers=headers).json()
encrypted = response.get('encrypted')

# Extract video URL
if encrypted:
    # Get required values to decode
    encrypted_data = quote_plus(response['sources'])
    nonce_encoded = quote_plus(nonce)
    key_encoded = quote_plus(key)

    # Decoding is handled on the server side to avoid PRNG-related issues in Python
    # Original server-side implementation reference: https://github.com/yogesh-hacker/yogesh-hacker/blob/main/js/videostr.js
    decode_url = f"{decode_url}?encrypted_data={encrypted_data}&nonce={nonce_encoded}&secret={key_encoded}"
    response = requests.get(decode_url, allow_redirects=True).text
    video_url = re.search(r'\"file\":\"(.*?)\"', response).group(1)
else:
    video_url = response['sources'][0]['file']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")
