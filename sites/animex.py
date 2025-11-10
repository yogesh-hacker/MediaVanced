import re
import os
import json
import time
import base64
import random
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse

'''
Supports:
https://animex.one/
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
base_url = 'https://animex.one/watch/your-name-21519-episode-1'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
aes_key_hex = "cb0508cc59c8d21edc8151662da35af851e4e630ad4798a29b95a06d2c07a82b"
xor_key_hex = "085e0b2d496881f8e52ba8d7e405be27"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Utility Functions
''' Perform repeating-key XOR on the input byte sequenc. '''
def xor_bytes(data: bytes, key: bytes) -> bytes:
    result = bytearray(len(data))
    for i in range(len(data)):
        result[i] = data[i] ^ key[i % len(key)]
    return bytes(result)

# Get content info
content_info = re.search(r'\/.*?(\d+)-episode-(\d+)', base_url)
media_id = content_info.group(1)
episode_num = content_info.group(2)

# Prepare payload
payload = {
    "id": int(media_id),
    "host": "pahe",
    "epNum": episode_num,
    "type": "sub",
    "cache": "true",
    "timestamp": int(time.time() * 1000)
}
plaintext = json.dumps(payload)

# Convert hex keys to bytes
aes_key_bytes = bytes.fromhex(aes_key_hex)
xor_key_bytes = bytes.fromhex(xor_key_hex)

# Generate 12-byte IV for AES-GCM
iv_bytes = os.urandom(12)

# Prepare payload bytes and apply XOR
payload_bytes = plaintext.encode("utf-8")
xored_payload = xor_bytes(payload_bytes, xor_key_bytes)

# Encrypt with AES-GCM
cipher = AES.new(aes_key_bytes, AES.MODE_GCM, nonce=iv_bytes)
ciphertext, tag = cipher.encrypt_and_digest(xored_payload)

# Combine IV + ciphertext + tag
encrypted_blob = iv_bytes + ciphertext + tag

# Encode URL-Safe and Get streaming data
encoded = base64.urlsafe_b64encode(encrypted_blob).decode().rstrip("=")
stream_info = requests.get(f'{default_domain}/api/anime/sources/{encoded}', headers=headers).json()

# Parse video URL
video_url = stream_info.get('sources')[0].get('url')

# Print Results
print("\n" + "#"*25 + "\n" + "#"*25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#"*25 + "\n" + "#"*25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")