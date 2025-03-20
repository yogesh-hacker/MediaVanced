import requests
import re

## Library v1.2 ##

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

## WASM? Well tried!
## Sorry this is more easy than custom encryption methods
## Hahahah!!!

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

payload = {
    "input": encrypted_data,
    "key": "ojl,&[y^-{cH!ux1"
}

wasm_decode_api = "https://light-snake-34.deno.dev/"
# The quota might exceed; it's recommended to create your own.  
# To access the API source code, visit:  
# https://yogesh-hacker.github.io/yogesh-hacker/wasm_api_playerx.js

# Send POST request with JSON headers
response = requests.post(wasm_decode_api, json=payload, headers={"Content-Type": "application/json"}).text

# Get decoded output
decrypted_data = response.encode().decode('unicode_escape')

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