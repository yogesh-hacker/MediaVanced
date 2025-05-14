import requests
from urllib.parse import urlparse
from base64 import b64decode
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

## Func ID: QOn7xhY ##

'''
Supports:
https://chillx.top/
https://boosterx.stream/
https://playerx.stream/
https://vidstreaming.xyz/
https://raretoonsindia.co/
https://plyrxcdn.site/
https://newer.stream/
https://mov18plus.cloud/
'''

# @PlayerX, After a long time!! with OG methods
# 25th attempt, I love you! :)
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
base_url = "https://plyrxcdn.site/v/17klI4BlD87T/"
user_agent = "Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent
}

# Set Up Session for all requests(Optional)
session = requests.Session()
session.headers.update(headers)

# Fetch page and extract encrypted data
response = session.get(base_url).text
match = re.search(r"(?:const|let|var|window\.\w+)\s+\w*\s*=\s*'(.*?)'", response)
if not match:
    exit(print("No encrypted data found."))
encrypted_data = match.group(1)
password = "#w8pukc]MoiBhH1{QlwOFF^I7pU]N9q^"

# Extract IV(Initialization Vector) and Encrypted Data
decoded_bytes = b64decode(encrypted_data)
iv_bytes = decoded_bytes[:16]
encrypted_bytes = decoded_bytes[16:]
key_bytes = password.encode('utf-8')

# Decrypt using AES-CBC
cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
decrypted_bytes = cipher.decrypt(encrypted_bytes)

# Remove PKCS7 padding and decode the decrypted data to plaintext
decrypted_data = unpad(decrypted_bytes, AES.block_size).decode("utf-8")

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
