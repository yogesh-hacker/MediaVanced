import re
import random
import base64
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import pad


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
base_url = "https://111movies.com/movie/533535"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent,
    "Content-Type": "font/woff",
    "X-Requested-With": "XMLHttpRequest"
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input):
    src = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    dst = "2xwYJGjOibPtCBu3lUNzL_HrQTVK0gFymven4RShWA6f71IcXs-MZ5EaoqkD8pd9"
    trans = str.maketrans(src, dst)
    b64 = base64.b64encode(input.encode()).decode().replace('+', '-').replace('/', '_').replace('=', '')
    return b64.translate(trans)

# Fetch page content
response = requests.get(base_url, headers=headers).text

# Extract raw data
match = re.search(r'{\"data\":\"(.*?)\"', response)
if not match:
    exit(print("No data found!"))
raw_data = match.group(1)


# AES encryption setup
key_hex = "92602fba85ae08969373a50448391cdbccadeb40be09abb17007861049944842"
iv_hex = "1e933f03e2fb9d2e77f457ac1645f33d"
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data).hex()

# XOR operation
xor_key = bytes.fromhex("edc5e93586d7")
xor_result = ''.join(chr(ord(char) ^ xor_key[i % len(xor_key)]) for i, char in enumerate(aes_encrypted))

# Custom encoded string
encoded_final = custom_encode(xor_result)

# Make final request
static_path = "APA91t9PoZwHV2WyucaGbKSpxJx7c_VYAYWOXlI8WCB-gTWcvz88bY9PMJ7I30nJayTEJg4AAtk0Gaa6D4V8FJQ9_Io3CtM9law2xptLLoKR8eD8slNP3WwL9x7juFBjXNVr9ciqrMoF2CV9xfmhITgEl6-zqVyecEO801em3fs4_osx2fWihKO/48bbb48dc848f14d2754754d197d939dbab4da99/i/bawose/laf/1181c071/1000037950406033/01ade2fbcf5203de7bc999e631258e3da61441cfe877770fa4cdc28c9971c8cf"
api_servers = f"https://111movies.com/{static_path}/{encoded_final}/sr"
response = requests.get(api_servers, headers=headers).json()

# Select a random server
server = random.choice(response)['data']
api_stream = f"https://111movies.com/{static_path}/{server}"
response = requests.get(api_stream, headers=headers).json()

# Extract video URL
video_url = response['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")