import time
import base64
import hashlib
import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from urllib.parse import urlparse
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

'''
Supports:
https://ployan.com/
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
base_url = 'https://ployan.live/watch/?v11#WGVWTVJMRC8rK2hJWERTeVpNQ1d0V084VmxYcVYwNE5CVlFFODZGaE1DRzhYQ1JobFB0ZE9vOTdHVTJYY0tRVUROakx2UDdUSWJJPQ'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Fetch Cloudflare trace
response = requests.get("https://vido-player.pages.dev/cdn-cgi/trace", headers=headers).text

# Extract encrypted hash
encrypted_hash = base_url.split("#")[-1]

# Parse trace response
trace_info = dict(line.split("=")for line in response.strip().split("\n"))

# Generate decryption key
country_code = trace_info.get('loc')
decrypt_key = hashlib.sha256(country_code.encode()).digest()

# Fix Base64 padding
encrypted_hash += "=" * (-len(encrypted_hash) % 4)

# Decode first layer
first_layer = base64.b64decode(encrypted_hash).decode('utf-8')

# Decode encrypted payload
encrypted_data = base64.b64decode(first_layer)

# Extract AES-GCM components
nonce = encrypted_data[:12]
ciphertext = encrypted_data[12:-16]
auth_tag = encrypted_data[-16:]

# Decrypt payload
cipher = AES.new(decrypt_key, AES.MODE_GCM, nonce=nonce)
plaintext = cipher.decrypt_and_verify(ciphertext, auth_tag).decode()

# Update timestamp
payload_parts = plaintext.split("+")
current_time = int(time.time())
updated_plaintext = f"{payload_parts[0]}+{payload_parts[1]}+{payload_parts[2]}+{current_time}"

# Generate encryption key
password = "player"
salt = get_random_bytes(8)
encrypt_key = PBKDF2(password, salt, dkLen=32, count=1000, hmac_hash_module=SHA256)

# Create AES-GCM cipher
iv = get_random_bytes(12)
cipher = AES.new(encrypt_key, AES.MODE_GCM, nonce=iv)

# Encrypt payload
encrypted_payload, auth_tag = cipher.encrypt_and_digest(updated_plaintext.encode())

# Build final payload
payload = f'{salt.hex()}-{iv.hex()}-{encrypted_payload.hex()}{auth_tag.hex()}'

# Get streaming token 
api_url = f'{default_domain}/get/{payload}'
response = requests.get(api_url, headers=headers).json()
token = response.get('info')

# Extract video URL
video_url = f'{default_domain}/hls/{token}/master.m3u8'

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
