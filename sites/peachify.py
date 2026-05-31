import re
import json
import base64
import random
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse

'''
Supports:
https://peachify.top/
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
base_url = 'https://peachify.top/embed/tv/93405/1/1'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
decryption_key_hex = "a8f2a1b5e9c470814f6b2c3a5d8e7f9c1a2b3c4d5e3f7a8b8cad1e2d0a4d5c5b"
streaming_servers = [
    {
        "label": "Iron",
        "path": "moviebox",
        "api": "https://uwu.eat-peach.sbs"
    },
    {
        "label": "Spider",
        "path": "holly",
        "api": "https://usa.eat-peach.sbs"
    },
    {
        "label": "Wolf",
        "path": "air",
        "api": "https://usa.eat-peach.sbs"
    },
    {
        "label": "Multi",
        "path": "multi",
        "api": "https://usa.eat-peach.sbs"
    },
    {
        "label": "Dark",
        "path": "net",
        "api": "https://uwu.eat-peach.sbs"
    }
]
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Utility Functions
def decode_base64url(data: str) -> bytes:
    """Decode Base64URL string."""
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

# Extract media identifier from embed URL
media_path = base_url.split('/embed/')[-1]

# Select target streaming backend
selected_server = streaming_servers[1]

# Retrieve encrypted playback payload
api_endpoint = f'{selected_server.get('api')}/{selected_server.get('path')}/{media_path}'
response = requests.get(api_endpoint, headers=headers).json()
encrypted_payload = response.get('data')

# Parse AES-GCM components
nonce_b64, ciphertext_b64, auth_tag_b64 = encrypted_payload.split(".")
nonce = decode_base64url(nonce_b64)
ciphertext = decode_base64url(ciphertext_b64)
authentication_tag = decode_base64url(auth_tag_b64)

# Decrypt payload using AES-256-GCM
decryption_key = bytes.fromhex(decryption_key_hex)
cipher = AES.new(decryption_key, AES.MODE_GCM, nonce=nonce)
plaintext = cipher.decrypt_and_verify(ciphertext, authentication_tag)

# Parse playback metadata
playback_data = json.loads(plaintext.decode('utf-8'))
available_sources = playback_data.get('sources', [])
if available_sources:
    random_source = random.choice(available_sources)

# Extract video URL
video_url = random_source.get('url')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")
