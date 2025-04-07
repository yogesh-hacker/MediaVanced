import requests
import re
import base64
import hashlib
from nacl.public import PrivateKey
from nacl.encoding import RawEncoder
from nacl.secret import SecretBox
from nacl.exceptions import CryptoError
from nacl.bindings import crypto_scalarmult
import binascii
import os

## Library v5.3 ##

'''
Supports:
https://vidstreamnew.xyz/
https://moviesapi.club/
https://chillx.top/
https://boosterx.stream/
https://playerx.stream/
https://vidstreaming.xyz/
https://raretoonsindia.co/
https://plyrxcdn.site/
https://newer.stream/
'''

# @PlayerX, Nice choice with Diffie-Hellman! 🔐
# It was new to me—that’s why it took some time ⏳😅
# No worries, give it another shot with something fresh next time! 🔁✨
# 22nd attempt at cracking you—haha! 💥😂
# Contact: businesshackerindia@gmail.com 📧

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
base_url = "https://raretoonsindia.co/v/zecLyCAzldEL/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
headers = {
    "Referer": "https://raretoonsindia.co",
    "User-Agent": user_agent
}

# Utility Functions
# Generate a 12-byte random hex nonce
def generate_nonce():

    return binascii.hexlify(os.urandom(12)).decode()

# Set Up Session for all requests(Optional)
session = requests.Session()
session.headers.update(headers)

# Fetch page and extract encrypted data
response = session.get(base_url).text
match = re.search(r"(?:const|let|var|window\.\w+)\s+\w*\s*=\s*'(.*?)'", response)
if not match:
    exit(print("No encrypted data found."))

encrypted_data = match.group(1)

# Generate client's key pair
client_private_key = PrivateKey.generate()
client_public_key = client_private_key.public_key

# Encode public key to base64 string
client_pubkey_raw = client_public_key.encode(encoder=RawEncoder)
client_pubkey_b64 = base64.b64encode(client_pubkey_raw).decode()

# ----------- #
# ----------- #

# Step 1: Prepare token by sending public key and nonce
data = {
    "nonce": generate_nonce(),
    "client_public_key": client_pubkey_b64
}

response = session.post("https://raretoonsindia.co/api/1.2/prepair-token.php", json=data).json()

# Get necessary data
pre_token = response['pre_token']
csrf_token = response['csrf_token']
server_pubkey_b64 = response['server_public_key']

# ----------- #
# ----------- #

# Step 2: Request access token using pre_token and csrf
initial_nonce = generate_nonce()
data = {
    "nonce": initial_nonce,
    "pre_token": pre_token,
    "csrf_token": csrf_token
}

response = session.post("https://raretoonsindia.co/api/1.2/create-token.php", json=data).json()

access_token = response['token']

# ----------- #
# ----------- #

# Step 3: Send encrypted data with required tokens
data = {
    "token": access_token,
    "initial_nonce": initial_nonce,
    "nonce": generate_nonce(),
    "csrf_token": csrf_token,
    "pre_token": pre_token,
    "encrypted_data": encrypted_data
}

response = session.post("https://raretoonsindia.co/api/1.2/process-token.php", json=data).json()

# Step 4: Derive shared key using server public key and client's private key
server_pubkey_raw = base64.b64decode(server_pubkey_b64)
shared_secret = crypto_scalarmult(client_private_key.encode(), server_pubkey_raw)
symmetric_key = hashlib.sha256(shared_secret).digest()

# Step 5: Decode payload and decrypt using SecretBox
enc_payload = base64.b64decode(response['encrypted_payload'])
enc_nonce = base64.b64decode(response['nonce'])

# Decode the final result
decrypted_data = SecretBox(symmetric_key).decrypt(enc_payload, enc_nonce).decode('utf-8') 

# Extract video URL
video_match = re.search(r'(?:file\s*:\s*|"file"\s*:\s*)"(https?://[^"]+)"', decrypted_data)
video_url = video_match.group(1) if video_match else exit(print("No video URL found."))

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")
