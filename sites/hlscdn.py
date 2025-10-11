import re
import json
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from urllib.parse import urlparse
from Crypto.Protocol.KDF import PBKDF2

'''
Supports:
https://hlscdn.xyz/
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
base_url = "https://hlscdn.xyz/e/299686-03"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent,
    "Accept": "text/plain, */*; q=0.01",
    "Content-Type": "text/plain",
    "X-Requested-With": "XMLHttpRequest",
}

# Fetch page content
response = requests.get(base_url, headers=headers).text

# Get token, payload and encrypted data
payload = re.search(r'window\.kaken=\"(.*?)\"', response).group(1)
auth_token = re.search(r'ps=\"(.*?)\"', response).group(1)
password = re.search(r'pd=\"(.*?)\"', response).group(1)
response = requests.post(f'https://hlscdn.xyz/api/?p={auth_token}', data=payload, headers=headers).text

# Prepare decryption parameters
encrypted = base64.b64decode(response)
salt = encrypted[:16]
ciphertext = encrypted[16:]

# Derive Key and IV (PBKDF2)
key_material = PBKDF2(password, salt, dkLen=48, count=10000, hmac_hash_module=SHA256)
key = key_material[:32]
iv = key_material[32:]

# Decrypt encrypted data(AES-CBC)
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_bytes = cipher.decrypt(ciphertext)

# Remove PKCS#7 padding
pad_len = decrypted_bytes[-1]
decrypted_data = decrypted_bytes[:-pad_len]
json_data = json.loads(decrypted_data.decode())

# Extract video URL
video_url = json_data.get('embed_url')

print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")