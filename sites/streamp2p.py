import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import json

'''
Supports:
https://multimovies.p2pplay.pro/
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
base_url = 'https://multimovies.p2pplay.pro/#pw8kx'
default_domain = 'https://multimovies.p2pplay.pro'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
headers = {
    'Referer': 'https://multimovies.p2pplay.pro/',
    'User-Agent': user_agent
}

# Fetch response
response = requests.get(base_url, headers=headers).text
video_id = base_url.split("#")[-1]

# Get encrypted video info from API
api = f'{default_domain}/api/v1/video?id={video_id}'
encrypted_data = requests.get(api, headers=headers).text

# Decrypt Data using AES-CBC
password = "kiemtienmua911ca"
iv = "1234567890oiuytr"

# Ensure key and IV are 16 bytes
key = password.encode('utf-8')
iv = iv.encode('utf-8')

# Convert hex to bytes
encrypted_bytes = bytes.fromhex(encrypted_data)

# Decrypt using AES CBC
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_bytes = cipher.decrypt(encrypted_bytes)

# Remove padding (PKCS7)
decrypted_json = unpad(decrypted_bytes, AES.block_size).decode('utf-8')
decrypted_data = json.loads(decrypted_json)

# Extract video URL
video_url = decrypted_data['source']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")