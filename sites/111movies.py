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
    "X-CSRF-Token": "4gglJgjvVNM6juEW0kEGdFTCf0ze4hYf",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input):
    src = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    dst = "PfWkLGQ1OY4m5wBTjy7IrngX0vcxERz_2U-i9hqpNDuKJtMo6lVdaeZ3AFSHb8sC"
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
key_hex = "8d0badc4081f89a3342549f3a68f5261a4438bd4e607871054b86116d99506a7"
iv_hex = "4ac971b2f09714ed29a9ad50084a3c34"
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data).hex()

# XOR operation
xor_key = bytes.fromhex("3115d3da3380")
xor_result = ''.join(chr(ord(char) ^ xor_key[i % len(xor_key)]) for i, char in enumerate(aes_encrypted))

# Custom encoded string
encoded_final = custom_encode(xor_result)

# Make final request
static_path = "f/1000001283280351/4e814452/cu/vacpuh/42a0e173-fb2d-50b0-bae4-1477e322b432/96966a8d451b1a19fd21afd3a51ade62dfa37d63"
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