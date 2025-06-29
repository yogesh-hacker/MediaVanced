import re
import json
import base64
import hashlib
import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from urllib.parse import urlparse

'''
Supports:
https://videostr.net/
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
provider_url = 'https://flixhq.tube/ajax/episode/sources/2521753'
# https://videostr.net/embed-1/v2/e-1/<VIDEO_ID>?z=
base_url = requests.get(provider_url).json()['link']
key_url = "https://raw.githubusercontent.com/yogesh-hacker/MegacloudKeys/refs/heads/main/keys.json"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
headers = {
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": default_domain,
    "User-Agent": user_agent
}

# Utility Functions


def openssl_key_iv(password, salt, key_len=32, iv_len=16):
    # Implements OpenSSL's EVP_BytesToKey derivation
    d = d_i = b""
    while len(d) < key_len + iv_len:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_len], d[key_len:key_len + iv_len]


def decrypt_openssl(enc_base64, password):
    data = base64.b64decode(enc_base64)
    assert data[:8] == b"Salted__"
    salt = data[8:16]
    key, iv = openssl_key_iv(password.encode(), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(data[16:])
    # Remove PKCS7 padding
    padding_length = decrypted[-1]
    return decrypted[:-padding_length].decode()

# Extract captions


def print_captions(tracks):
    captions = []
    if tracks:
        for track in tracks:
            if track.get('kind') == 'captions':
                label = track.get('label', 'Unknown')
                url = track.get('file', 'URL not available')
                captions.append({'label': label, 'url': url})
    return captions


# Fetch initial response
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Get file ID
video_tag = soup.select_one('#megacloud-player')
if not video_tag:
    exit(print(f'{Colors.fail}Looks like URL expired!{Colors.endc}'))
file_id = video_tag['data-id']

# Get encrypted data
response = requests.get(
    f'{default_domain}/embed-1/v2/e-1/getSources?id={file_id}', headers=headers).json()
encrypted = response['sources']

# Check if the response contains captions
tracks = response['tracks'] if 'tracks' in response else None
# Extract captions if available
captions = print_captions(tracks)

# Get Password
response = requests.get(key_url).json()
password = response['vidstr']

# Decrypt encrypted data
decrypted_data = decrypt_openssl(encrypted, password)

# Extract video URL
json_data = json.loads(decrypted_data)
video_url = json_data[0]['file']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("-" * 25)
if captions:
    print("\nCaptions:")
    for caption in captions:
        print(
            f"- {caption['label']}: {Colors.okblue}{caption['url']}{Colors.endc}")
print(f"\n{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")
