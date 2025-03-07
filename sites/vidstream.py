import requests
import re
import base64
import hashlib
from Crypto.Cipher import AES


## Library v6.4 ##

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


## Well done! 👏 This time, you really implemented some top-tier security.  
## But unfortunately for you, I’ve already broken through.  
## AES-GCM? 😂 Nice attempt!  
## Am I late? Yeah, but only because I was busy with other projects.


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
    "Referer": "https://vidstreamnew.xyz",
    "User-Agent": user_agent
}

# Fetch response
response = requests.get(base_url, headers=headers).text

# Extract encrypted data
match = re.search(r"(?:const|let|var|window\.(?:Delta|Alpha|Ebolt))\s+\w*\s*=\s*'(.*?)'", response)
if not match:
    exit(print("No encrypted data found."))

encrypted_data = match.group(1)

#Decode base64-encoded encrypted data
decoded_bytes = base64.b64decode(encrypted_data)

# Extract Initialization Vector (IV), Authentication Tag, and Ciphertext
iv = decoded_bytes[:12]  
auth_tag = decoded_bytes[12:28]  
ciphertext = decoded_bytes[28:]

# Convert base64-encoded password to a SHA-256 encryption key
password_base64 = "fnBmd19PVzRyfSFmdWV0ZQ=="
password = base64.b64decode(password_base64).decode('utf-8')
key = hashlib.sha256(password.encode()).digest()

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
