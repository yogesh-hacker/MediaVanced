import re
import os
import json
import time
import base64
import string
import random
import hashlib
import requests
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

'''
Supports:
https://hexa.watch/
'''

# @Hexa, The cookie was yummy! Do you want the celestial taste?

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
base_url = "https://hexa.watch/watch/movie/284054"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
headers = {
    "Referer": "https://hexa.watch/",
    "Accept": "*/*",
    "User-Agent": user_agent
}
media_type = 'movie' if 'movie' in base_url else 'tv'
match = re.search(r'/(\d+)(?:/(\d+)/(\d+))?', base_url)
media_id = f"{match.group(1)}/{match.group(2)}/{match.group(3)}" if media_type == "tv" else match.group(1)


# Utility Functions
''' SHA256 Hasher '''
def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

''' CryptoJS like AES-CBC encryption '''
def aes_encrypt(plaintext: str, password: str) -> str:
    salt = os.urandom(8)
    derived = b''
    while len(derived) < (32 + 16):
        last = derived[-16:]  # last IV block or empty
        md = MD5.new()
        md.update(last + password.encode('utf-8') + salt)
        derived += md.digest()
    key, iv = derived[:32], derived[32:48]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    encrypted = b"Salted__" + salt + ciphertext
    return base64.b64encode(encrypted).decode('utf-8')

''' CryptoJS like AES-CBC decryption '''
def aes_decrypt(ciphertext_b64: str, password: str) -> str:
    encrypted = base64.b64decode(ciphertext_b64)
    if not encrypted.startswith(b"Salted__"):
        raise ValueError("Invalid encrypted data format")
    
    salt = encrypted[8:16]
    ciphertext = encrypted[16:]

    derived = b''
    while len(derived) < (32 + 16):
        last = derived[-16:]  # last IV block or empty
        md = MD5.new()
        md.update(last + password.encode('utf-8') + salt)
        derived += md.digest()
    key, iv = derived[:32], derived[32:48]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)
    return plaintext.decode('utf-8')


# Core scraping logic begins here
# Generate timestamp (ms) and random 13-char base36 string
timestamp = int(time.time() * 1000)
random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=13))

# Primary and secondary encryption keys (Base64-encoded)
key_main = "aG9wZSB5b3UgaGFkIGZ1biBkZWNyeXB0aW5nIHRoaXMgZ29vZCBqb2Igbm93IGdvIGFzayB5b3VyIG1vbSBmb3IgYSBjb29raWU="
key_secondary = "b21nIHlvdSBmb3VuZCBteSBrZXkgcGxlYXNlIGdvIHRvdWNoIGdyYXNzIHlvdSBsaXR0bGUgZmF0IGJhc2VtZW50IG1vbmtleQ=="

# First layer: original payload with checksum
payload_lvl1 = {
    "type": media_type,
    "id": media_id,
    "timestamp": timestamp,
    "random": random_str,
    "checksum": sha256(f"{media_type}{media_id}{timestamp}{random_str}{key_main}")
}

# Second layer: encrypt lvl1 with secondary key
payload_lvl2 = {
    "data": aes_encrypt(json.dumps(payload_lvl1), key_secondary),
    "timestamp": timestamp
}

# Third layer: encrypt lvl2 with combined key
payload_lvl3 = {
    "data": aes_encrypt(json.dumps(payload_lvl2), f"{key_secondary}{timestamp}"),
    "timestamp": timestamp,
    "random": random_str
}

# Final token: encrypt lvl3 with main key
auth_token = aes_encrypt(json.dumps(payload_lvl3), key_main)

# Set request headers
headers['x-auth'] = auth_token

# Send request
response = requests.get("https://heartbeat.hexa.watch", headers=headers).json()
encrypted_data = response['encrypted']

# Decrypting layers
lvl3 = json.loads(aes_decrypt(encrypted_data, key_main))
lvl2 = json.loads(aes_decrypt(lvl3['data'], f"{key_secondary}{lvl3['timestamp']}"))
lvl1 = json.loads(aes_decrypt(lvl2['data'], key_secondary))

# Extract Video URL(s)
decrypted_data = lvl1['data']['sources']
video_url = random.choice(decrypted_data)['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")