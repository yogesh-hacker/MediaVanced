import requests
import re
import base64
from Crypto.Cipher import AES
import binascii
from Crypto.Util.Padding import unpad


## Func ID: AkeGtWh ##


## @Chillx, did you really think I spared (left) you?
## No, I had exams, that's why! 😁 But now, I'm back for you!
## Using modules? That's good, but nothing can stop me.

'''
Supports:
https://vidstreamnew.xyz/
https://moviesapi.club/
https://chillx.top/
https://boosterx.stream/
https://playerx.stream/
https://vidstreaming.xyz/
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
base_url = "https://vidstreaming.xyz/v/Gel3fC9MllfL/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
headers = {
    "Referer": "https://vidstreamnew.xyz",
    "User-Agent": user_agent
}

# Fetch response
response = requests.get(base_url, headers=headers).text

# Extract encrypted data
match = re.search(r"(?:const|let|var|window\.(?:Delta|Alpha))\s+\w*\s*=\s*'(.*?)'", response)
if not match:
    exit(print("No encrypted data found."))

encrypted_data = match.group(1)

#Decode base64-encoded encrypted data
bytes_data = base64.b64decode(encrypted_data)

# Convert to uint8 array equivalent (byte slice)
iv = bytes_data[:16]
ciphertext = bytes_data[16:]

# Convert hex key to bytes
key_base64 = "ZmJlYTcyMGU5MDY0NDE3Mzg1MDc0MjMzOThiYTcwMjg5ZTQwNjJmZTU2NGFhNTU5OTY5OWZhNjA2NDVmNzdjZA=="
key_hex = base64.b64decode(key_base64).decode('utf-8')
key = binascii.unhexlify(key_hex)

# Decrypt using AES in CBC mode
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)

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
