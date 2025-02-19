import requests
import re
import base64
import array

## Func ID: DKixG_Y ##



## Due to my exams, it's taken longer than expected 😤
## Chillx, f##k you 😒
## Let me finish my exams from 19th to 22nd February
## Then I'll get back to you, you stupids!!

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
    "User-Agent": user_agent,
    "priority":"u=0, i",

}
password = "^F2,[o8}txnv97TP"

# Fetch response
response = requests.get(base_url, headers=headers).text

# Extract encrypted data
match = re.search(r"(?:const|let|var)\s+\w+\s*=\s*'(.*?)'", response)
if not match:
    exit(print("No encrypted data found."))

encrypted_data = match.group(1)

# Convert hex values to bytes
byte_data = bytes(int(encrypted_data[i:i + 2], 16) for i in range(0, len(encrypted_data), 2))

# RC4 Decryption Proccess
def rc4_decrypt(key, encrypted_data):
    # Initialize the S array (State array)
    key_length = len(key)
    S = list(range(256))  # State array
    j = 0
    
    # Key Scheduling Algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + ord(key[i % key_length])) % 256
        S[i], S[j] = S[j], S[i]
    
    # Pseudo-Random Generation Algorithm (PRGA)
    i = 0
    j = 0
    decrypted_data = []
    
    for byte in encrypted_data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        decrypted_data.append(byte ^ K)
    
    return bytes(decrypted_data)

# Decrypt and proceed
decrypted_data = rc4_decrypt(password, byte_data).decode('utf-8')

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
