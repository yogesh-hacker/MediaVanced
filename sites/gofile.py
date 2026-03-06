import time
import math
import hashlib
import requests
from urllib.parse import urlparse

'''
Supports:
https://gofile.io/
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
base_url = "https://gofile.io/d/UkC1G6"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
guest_account_url = "https://api.gofile.io/accounts"
browser_language = "en-GB"
secret = "gf2026x"
headers = {
    "Referer": "https://gofile.io/",
    "User-Agent": user_agent
}

# Extract the file ID from the URL
parsed_url = urlparse(base_url)
file_id = parsed_url.path.split('/')[-1]

# Get guest account token
token = None
try:
    response = requests.post(guest_account_url, data={})
    response.raise_for_status()
    response = response.json()
    token = response.get('data', {}).get('token')
    headers['Authorization'] = f'Bearer {token}'
except (requests.RequestException, ValueError) as e:
    exit(print(f"ERROR: {str(e)}"))

# Current 4-hour interval
interval = str(math.floor(time.time() / 14400))

# Build message and hash it
message = "::".join([user_agent, browser_language, token, interval, secret])
hashed_token = hashlib.sha256(message.encode('utf-8')).hexdigest()

# Set Hash as Token
headers["X-BL"] = browser_language
headers["X-Website-Token"] = hashed_token


# Get file link
response = requests.get(f"https://api.gofile.io/contents/{file_id}?contentFilter=&page=1&pageSize=1000&sortField=name&sortDirection=1", headers=headers).json()
children = response.get('data', {}).get('children', {})
if not children:
    raise ValueError("No children found in the response data")

# Extract video URL
first_child_key = list(children.keys())[0]
video_url = children[first_child_key]['link']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Cookie: {Colors.endc}accountToken={token}")
print("\n")
