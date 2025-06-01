import re
import json
import random
import base64
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import pad


'''
Supports:
https://111movies.com/
'''

# @111movies, Kaalchoddu, haha :)

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
    "Content-Type": "application/vnd.api+json",
    "X-CSRF-Token": "6V0pzHm1pehBhSGG9UxAdLJ4QezSBdMJ",
    "X-Requested-With": "XMLHttpRequest"
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input):
    src = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    dst = "K9jcxzyd3NeYCuvtF18DbWM-wRHh6qnrZA5JEUISgp_XfT20aBlL7GQV4OoisPkm"
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
key_hex = "a10e5798728e186d71dbb25c85b70006595c43ebc56077caee5c46fdaec034f9"
iv_hex = "82562b2cf22038d3daa1770234c63a04"
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data).hex()

# XOR operation
xor_key = bytes.fromhex("c679ea0d")
xor_result = ''.join(chr(ord(char) ^ xor_key[i % len(xor_key)]) for i, char in enumerate(aes_encrypted))

# Custom encoded string
encoded_final = custom_encode(xor_result)

# Make final request
static_path = "APA91KRy2oMU649_pFh2ZLjN2jVZtD-qDAy3sOacFLYmJfyYl8Uy0u1qOOf5kMnYVr4r7yKbh97hBMaRy7i5m78DvYx2g5C16kzq3JW0swcaBhaA-qvfPrSyu_hoW3vXENKQSkVPgTJvaoR-CUGW6Ti4DIzfXOhuSQA6NZOAlDIbkAbRUGrWtnN/k/c2a03ccc-92bb-5745-94e6-0257fb030698/jid/a8304842cd86af17206a5bf6ca4d1ff54e70a477/ir/06fbddd4ef9f2669eee5402279a9d9a00f6f0c1fd128089cab0e2a9528d3943e/f904b75d"
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