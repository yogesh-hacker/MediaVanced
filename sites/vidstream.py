import requests
import re

## Func ID: yaIm2u ##

'''
Supports:
https://vidstreamnew.xyz/
https://moviesapi.club/
https://chillx.top/
https://boosterx.stream/
https://playerx.stream/
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
base_url = "https://boosterx.stream/v/NGGJGqZKpllV/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
headers = {'Referer': base_url, 'User-Agent': user_agent}
password = "HG1I}V!u$IR6Rxdf"

# Fetch encrypted data
response = requests.get(base_url, headers=headers).text

# Extract encrypted data with regex
match = re.search(r"const\s+\w+\s*=\s*'(.*?)'", response)
if not match:
    print("No encrypted data found.")
    exit()

encrypted_data = match.group(1)

# Convert password to bytes
password_bytes = bytes(password, 'utf-8')

# Decrypt the data with XOR operation
decrypted_data = bytearray(
    [int(encrypted_data[i:i+2], 16) ^ password_bytes[i // 2 % len(password_bytes)]
     for i in range(0, len(encrypted_data), 2)]
).decode('utf-8', errors='ignore')

#Get the video file URL
video_url_pattern = r'(?:file\s*:\s*|"file"\s*:\s*)"(https?://[^"]+)"'
video_url_match = re.search(video_url_pattern, decrypted_data)

video_url = ""
if video_url_match:
    video_url = video_url_match.group(1)
else:
    print("No video URL found.")

# Print Results
print("\n" + "#"*25 + "\n" + "#"*25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#"*25 + "\n" + "#"*25)
print(f"{Colors.warning}### Please use the header \"Referer: https://vidstreamnew.xyz\" or the CDN host to access the URL, along with a User-Agent: {Colors.okcyan}[{user_agent}]{Colors.endc}\n")