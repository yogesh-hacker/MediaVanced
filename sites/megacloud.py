import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote_plus


'''
Supports:
https://megacloud.blog/
'''

# @Megacloud, @VideoStr || Am I look dumb to you? You cannot defeat me, note that!
# Still Confused? see PlayerX/Vidstream scraper

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
provider_url = 'https://hianime.to/ajax/v2/episode/sources?id=1155827'
base_url = requests.get(provider_url).json()['link'] # https://megacloud.blog/embed-2/v2/e-1/<VIDEO_ID>?k=1&autoPlay=1&oa=0&asi=1
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
decode_url ="https://script.google.com/macros/s/AKfycbx-yHTwupis_JD0lNzoOnxYcEYeXmJZrg7JeMxYnEZnLBy5V0--UxEvP-y9txHyy1TX9Q/exec"
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

# Get file ID
video_tag = soup.select_one('#megacloud-player')
if not video_tag:
    exit(print(f'{Colors.fail}Looks like URL expired!{Colors.endc}'))
file_id = video_tag['data-id']

# Get Nonce
match = re.search(r'\b[a-zA-Z0-9]{48}\b', response) or re.search(r'\b([a-zA-Z0-9]{16})\b.*?\b([a-zA-Z0-9]{16})\b.*?\b([a-zA-Z0-9]{16})\b', response)
nonce = ''.join(match.groups()) if match and match.lastindex == 3 else match.group() if match else None

# Get Password 
response = requests.get(key_url).json()
key = response['mega']

# Get encrypted data
response = requests.get(f'{default_domain}/embed-2/v3/e-1/getSources?id={file_id}&_k={nonce}', headers=headers).json()
encrypted = response['sources']

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