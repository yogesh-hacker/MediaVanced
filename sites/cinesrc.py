import re
import json
import base64
import requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from urllib.parse import urlparse
from datetime import datetime, timezone
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

'''
Supports:
https://cinesrc.st/
'''

# Many thanks to AzartX (https://github.com/AzartX47) for the guidance and support throughout the development of this scraper!

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
base_url = 'https://cinesrc.st/embed/movie/1084242'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}
server_action_token = requests.get('https://raw.githubusercontent.com/yogesh-hacker/MegacloudKeys/refs/heads/main/keys.json').json().get('cinesrc').get('getStream')
rsa_public_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCPnLvTpbxYFPHBv5TRj8uRaMlh
yp2ekzUgnyfMopVfnrsPgeC8mmM+tlmebZvDtA/zHGwYoAXViE7oiH57mbhVKrMp
T8OqE8sLlfppSDcEiLCfRAz8NfGu14gp7Uld9JiGMMeGSDNjtdEbAFD5jArxXbt9
cBBHg6Y5o40AM60WrwIDAQAB
-----END PUBLIC KEY-----"""
aes_key_b64 = "JWmlRlgGKC3MLQihZMqx/hW276z1FolQ8QRePYWhn/E="

# Ask user for Server selection
options = ["Nebula", "Storm", "Frost", "Breeze", "Rain", "Mist"]
while True:
    print("Select a server:")
    for i, server in enumerate(options, 1):
        print(f" {i}. {server}")
    
    choice = input("\nEnter the number of your choice: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        selected_server = options[int(choice) - 1].lower()
        print(f"Selected server: {selected_server}")
        break
    else:
        print("❌ Invalid choice, please try again.")

# Get content info
match = re.search(r'\/embed\/(.*?)\/(\d+)(?:\?s=(\d+)&e=(\d+))?', base_url)
if match:
    content_type = match.group(1)
    content_type = "show" if content_type == "tv" else content_type
    content_id, season, episode = (
        match.group(2),
        match.group(3) or '$undefined',
        match.group(4) or '$undefined'
    )

# Get token from server
response = requests.get(f'{default_domain}/api/signature', headers=headers).json()
token = response.get('token')

# Prepare encryption parameters
timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
path = urlparse(base_url).path
nonce = get_random_bytes(16)
salt = get_random_bytes(16)
iv = get_random_bytes(12)
aes_key = get_random_bytes(32)

# Prepare payload
payload = {
    'v': 1,
    'ts': timestamp,
    'ua': user_agent,
    'nonce': base64.b64encode(nonce).decode(),
    'salt': base64.b64encode(salt).decode(),
    'token': token,
    'path': path
}
plaintext = json.dumps(payload).encode()

# Encrypt Payload using AES-256-GCM
cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
encrypted, tag = cipher.encrypt_and_digest(plaintext)
aes_ciphertext = encrypted + tag

# Encrypt AES Key with RSA‑OAEP SHA256
rsa_key = RSA.import_key(rsa_public_key)
rsa_cipher = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA256)
rsa_encrypted_key = rsa_cipher.encrypt(aes_key)

# Build final encrypted request blob
encrypted_key_b64 = base64.b64encode(rsa_encrypted_key).decode()
iv_b64 = base64.b64encode(iv).decode()
ciphertext_b64 = base64.b64encode(aes_ciphertext).decode()

# Prepare Encrypted Blob
encrypted_blob = '.'.join(['v1', encrypted_key_b64, iv_b64, ciphertext_b64])

# Prepare Payload and Get Encrypted Streaming Data
request_payload = [content_id, content_type, season, episode, encrypted_blob, selected_server]
response = requests.post(base_url, data=json.dumps(request_payload), headers={**headers, 'next-action': server_action_token}).text

# Extract encrypted payload line
encrypted_line = response.splitlines()[1]
encrypted_payload = encrypted_line[2:].strip('"')

# Parse payload components
payload_parts = encrypted_payload.split(".")
version_tag = payload_parts[0]
iv_b64 = payload_parts[1]
ciphertext_b64 = payload_parts[2]

# Decode base64 values
iv_bytes = base64.b64decode(iv_b64)
ciphertext_with_tag = base64.b64decode(ciphertext_b64)
aes_key_bytes = base64.b64decode(aes_key_b64)

# Separate ciphertext and auth tag
ciphertext_bytes = ciphertext_with_tag[:-16]
auth_tag = ciphertext_with_tag[-16:]

# AES‑256‑GCM decryption
cipher = AES.new(aes_key_bytes, AES.MODE_GCM, nonce=iv_bytes)
plaintext_bytes = cipher.decrypt_and_verify(ciphertext_bytes, auth_tag)
plaintext = plaintext_bytes.decode("utf-8")

# Extract video URL
streaming_data = json.loads(plaintext).get('url')
video_url = streaming_data[0].get('url')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
