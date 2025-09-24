import json
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import unpad

'''
Supports:
https://cloudy.upns.one/
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
base_url = "https://cloudy.upns.one/#6srlr9"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent
}

# Get video ID and encrypted data
video_id = base_url.split('#')[-1]
api_url = f'{default_domain}/api/v1/video?id={video_id}'
encrypted_data = requests.get(api_url, headers=headers).text

# Convert hex key/IV and ciphertext to bytes
key_hex = "6b69656d7469656e6d75613931316361"
iv_hex = "313233343536373839306f6975797472"
key = bytes.fromhex(key_hex)
iv = bytes.fromhex(iv_hex)
ciphertext = bytes.fromhex(encrypted_data)

# Decrypt AES-128-CBC and remove PKCS#7 padding
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ciphertext)
decrypted_data = unpad(plaintext, AES.block_size)

# Extract video URL
stream_info = json.loads(decrypted_data)
video_url = stream_info.get('source')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")