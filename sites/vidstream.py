import requests
import re
import base64
import array

## Func ID: mOreFf ##

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
base_url = "https://boosterx.stream/v/NGGJGqZKpllV/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
headers = {
    "Referer": "https://vidstreamnew.xyz",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": user_agent
}
password = "~%aRg@&H3&QEK1QV"

# Fetch response
response = requests.get(base_url, headers=headers).text

# Extract encrypted data
match = re.search(r"const\s+\w+\s*=\s*'(.*?)'", response)
if not match:
    exit(print("No encrypted data found."))

encrypted_data = match.group(1)

# Decode Base64 to ASCII values
decoded_bytes = base64.b64decode(encrypted_data)
ascii_values = list(decoded_bytes)

key_bytes = ascii_values[:16]  # First 16 bytes as key
data_bytes = ascii_values[16:]  # Remaining as encrypted content

# Convert password to ASCII list
password_bytes = array.array("B", password.encode()).tolist()

# Decrypt data using XOR
decrypted_bytes = [
    data_bytes[i] ^ password_bytes[i % len(password_bytes)] ^ key_bytes[i % len(key_bytes)]
    for i in range(len(data_bytes))
]

# Convert decrypted bytes to string
decrypted_text = ''.join(chr(i) for i in decrypted_bytes)

# Extract video URL
video_match = re.search(r'(?:file\s*:\s*|"file"\s*:\s*)"(https?://[^"]+)"', decrypted_text)
video_url = video_match.group(1) if video_match else exit(print("No video URL found."))

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use header \"Referer: https://vidstreamnew.xyz\" and User-Agent: {Colors.okcyan}[{user_agent}]{Colors.endc}\n")
