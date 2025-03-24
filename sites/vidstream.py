import requests
import re
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

## Library v1.5 ##

'''
Supports:
https://vidstreamnew.xyz/
https://w1.moviesapi.club/
https://chillx.top/
https://boosterx.stream/
https://playerx.stream/
https://vidstreaming.xyz/
https://raretoonsindia.co/
https://plyrxcdn.site/
'''

# @PlayerX, Need any help?  
# 20th combo of cracking you, haha!  
# Contact: businesshackerindia@gmail.com

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
match = re.search(r"(?:const|let|var|window\.\w+)\s+\w*\s*=\s*'(.*?)'", response)
if not match:
    exit(print("No encrypted data found."))

encrypted_data = match.group(1)
password = "Gk^Gtn-cqrdpr05l@0snp+<7{KV>RDu"

# Get password bytes and generate key
decoded_bytes = bytes(ord(c) ^ 5 for c in password)
key = hashlib.sha256(decoded_bytes).digest()

# Decode base64 data
decoded_bytes = base64.b64decode(encrypted_data)
iv = decoded_bytes[36:52]
ciphertext = decoded_bytes[52:]

# Decrypt using AES
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext_padded = cipher.decrypt(ciphertext)

# Remove padding and decode  
decrypted_data = unpad(plaintext_padded, AES.block_size).decode()

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