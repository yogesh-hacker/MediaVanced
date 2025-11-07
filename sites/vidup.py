import re
import random
import base64
import requests
import cloudscraper
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import pad

'''
Supports:
https://vidup.to/
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
base_url = "https://vidup.to/movie/587412"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Accept": "*/*",
    "Referer": default_domain,
    "User-Agent": user_agent,
    "X-Csrf-Token": "r92mGaqV1ePy2Tz3Oy9mLvrETahmoeTm",
    "X-Requested-With": "XMLHttpRequest"
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input_bytes):
    source_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    target_chars = "5LkfH2dsVn-aWDqzJpRhFP8jilY9_wEANxZGCMT34y1XrecoUO6mSgu7Kt0bBQIv"
    translation_table = str.maketrans(source_chars, target_chars)
    encoded = base64.urlsafe_b64encode(input_bytes).decode().rstrip('=')
    return encoded.translate(translation_table)

# Initialize Cloudscraper session (bypasses Cloudflare)
scraper = cloudscraper.create_scraper()

# Fetch page content
response = scraper.get(base_url).text

# Extract raw data
match = re.search(r'\\"en\\":\\"(.*?)\\"', response)
if not match:
    exit(print("No data found!"))
raw_data = match.group(1)

# AES encryption setup
key_hex = '94cb23ee065f66267d176f68eb79571022f3b6099db41bf5bd2c5ab28c72ad43'
iv_hex = '73c97f3a1c06a117ee830eb8736cf64f'
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

# Encrypt raw data
cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data)

# XOR operation
xor_key = bytes.fromhex("b7abdb6a2ae613781bb6")
xor_result = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(aes_encrypted))

# Encode XORed data
encoded_final = custom_encode(xor_result)

# Get streaming servers
static_path = "hezushon/fun/e8b589ffffb5119301d2726e214693a07e7c98e9/APA918OZyDhFxerTsFz45sHyEvXxcVPVs0QulQGArl0lKahNWkvvLBnOQyLn4-nZzDs0qJ9MTC7FXsQVeZrw49Jfz79tgywFQXscK_tZaAMzI6WAZveztyn4HJAbeJ7ey6oJL7U_8s9DogiOulKN5V1EknVJ5_8kFGFxx0pk8Du-tvHDGXjtWgr"
data = {}
api_servers = f"https://vidup.to/{static_path}/uMo/{encoded_final}"
response = requests.get(api_servers, headers=headers).json()

# Select a random server
server = random.choice(response)['data']
api_stream = f"https://vidup.to/{static_path}/T2dQFY4Pn4lVEQ/{server}"
response = requests.get(api_stream, headers=headers).json()

# Extract video URL
video_url = response['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")