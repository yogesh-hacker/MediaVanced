import re
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
    "X-CSRF-Token": "9crboYhXqMxjX3CO6h9D9GmjD0TOyIwB",
    "Content-Type": "application/zip",
    "X-Requested-With": "XMLHttpRequest",
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input):
    src = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    dst = "MkY1udDxfeBTpO5FvV7SX0Lln9KUhm6Ci_WEawJRzG-Zo32N4s8IgtqbrcPAQjHy"
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
key_hex = "d32118507780dd88404e7b1ff6aa904c2d6dcb001d3b92253e4f69b4ff3ae08d"
iv_hex = "5508bd88ea7c230d4ee31334e1125bf4"
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data).hex()

# XOR operation
xor_key = bytes.fromhex("df8e4b")
xor_result = ''.join(chr(ord(char) ^ xor_key[i % len(xor_key)]) for i, char in enumerate(aes_encrypted))

# Custom encoded string
encoded_final = custom_encode(xor_result)

# Make final request
static_path = "1000047336362563/9f2cc71f630612dbecee371e8cafa6d430642eec/ce/vo/APA91xX-nSpP8INTQ12SjTpw_LooWDvsc2OEna30Naw-KkIuEnGF8_--c3YTItPsUJWZ3z0Zx7L6vJVh2VnWJUxpZ-Y7jP7E8RBcBQfQFZbmAsSlMCxAH9fzLPOHGieB03hxFtIg8LviAnD4VmS9FCxIjoICHtEiCmVRXEt2QcbSfl3oKjAyyJp/35e20f11/4545f944904f8b9c8ac584a5ec6f4ecb15a4018e0d34d11e95fe27dd84b7cda1/i"
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