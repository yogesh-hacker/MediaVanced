# abyss.py
import re
import json
import base64
import hashlib
import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from urllib.parse import urlparse


## VERSION: 1.2 ##

'''
Supports:
https://abysscdn.com/
https://hydraxcdn.biz/
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
base_url = "https://abysscdn.com/?v=etBDGEkak"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent
}

# Fetch and parse encoded data
response = requests.get(base_url, headers=headers).text
match = re.search(r'const\sdatas\s=\s\"(.*?)\"', response)
if not match:
    print("Error: No encoded data found!")
encoded_data = match.group(1)

# Decode
decoded_text = base64.b64decode(encoded_data).decode('latin-1')
data = json.loads(decoded_text)

# Extract the variables needed for the key
user_id = str(data['user_id'])
slug = data['slug']
md5_id = str(data['md5_id'])

# Create the hash seed and get the MD5 hex string
seed = f"{user_id}:{slug}:{md5_id}"
md5_hex = hashlib.md5(seed.encode('utf-8')).hexdigest()
key_bytes = md5_hex.encode('utf-8')

# The JS uses the first 16 bytes of that key as the AES-CTR Counter (IV)
iv_bytes = key_bytes[:16]

# Convert the characters in the media string back to raw bytes (again, using latin-1)
encrypted_media_bytes = data['media'].encode('latin-1')

# Decrypt the payload using AES-256-CTR
cipher = AES.new(key_bytes, AES.MODE_CTR, nonce=b'', initial_value=iv_bytes)
decrypted_bytes = cipher.decrypt(encrypted_media_bytes)

# Parse the decrypted bytes back into JSON
metadata_config = json.loads(decrypted_bytes.decode('utf-8'))

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"METADATA: {Colors.okgreen}{json.dumps(metadata_config, indent=2)}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### I really don't know how to play this shit!!!")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")
