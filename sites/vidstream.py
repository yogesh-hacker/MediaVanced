import requests
import re
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256


## Func ID: uO96yB ##

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
'''

## One Word: Dumb Ass

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

# Fetch response
response = requests.get(base_url, headers=headers).text

# Extract encrypted data
match = re.search(r"(?:const|let|var|window\.(?:Delta|Alpha|Ebolt|Flagon))\s+\w*\s*=\s*'(.*?)'", response)
if not match:
    exit(print("No encrypted data found."))

encrypted_data = match.group(1)

#Decode base64-encoded encrypted data
decoded_bytes = base64.b64decode(encrypted_data)

# Extract Salt, Initialization Vector (IV), Authentication Tag, and Ciphertext
salt = decoded_bytes[:16]
iv = decoded_bytes[16:28]
auth_tag = decoded_bytes[28:44]
ciphertext = decoded_bytes[44:]

# Generate a 256-bit key from a Base64 password using PBKDF2  
password_base64 = "SCkjX0Y9Vy5tY1FNIyZtdg=="
password = base64.b64decode(password_base64)
key = PBKDF2(password, salt, dkLen=32, count=999, hmac_hash_module=SHA256)

# Decrypt the data using AES-GCM
aes_cipher = AES.new(key, AES.MODE_GCM, iv)
decrypted_bytes = aes_cipher.decrypt_and_verify(ciphertext, auth_tag)

# Decrypt and proceed
decrypted_data = decrypted_bytes.decode('utf-8')

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
