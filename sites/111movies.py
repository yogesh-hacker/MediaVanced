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

# @111movies, What is the meaning of changing headers?
# @PlayerX knows my power.

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
    "Content-Type": "application/json-patch+json",
    "X-Csrf-Token": "h6mMOblBOJMUfn214Kbp7hbwmBa2c7YA",
    "X-Requested-With": "XMLHttpRequest"
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input):
    src = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    dst = "yRzqGAW8a5mcx9kvs2YO0lHtub_ZhpnKJX6PFdD3fr7UMgNILBjTCwi41EoQSVe-"
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
key_hex = "e019eef6c8f9086438608c0ecf63056d1eb382829b0202826eb0e0c85275bed3"
iv_hex = "24449dc8e60e17ce1f9ecd9b1ce6fb8b"
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data).hex()

# XOR operation
xor_key = bytes.fromhex("84a609d5fc5d69db22")
xor_result = ''.join(chr(ord(char) ^ xor_key[i % len(xor_key)]) for i, char in enumerate(aes_encrypted))

# Custom encoded string
encoded_final = custom_encode(xor_result)

# Make final request
static_path = "57a98bd8668da1a41c9a19cb5ff3b6d187da730d5430ffe91c54fb1f033e89c0/APA917twfMY4OADEIqKHNm5QpKCUH0ZmVnJxKgC6CmkCyfii28Zvm_vt3b7CoLy9xlk9PIqQqX3I0tkKm0niyFPC7TDe3PI_bAxub6ECacJkvj3xpziGVo1t56GJpboADn1P267-f-L493iKbL-J0xLVbHkehu-yzviOl_Cbefhmf4h36rZcBV3/4c309f39-b473-50af-82e3-69ed989f62f3/g"
api_servers = f"https://111movies.com/{static_path}/{encoded_final}/sr"
response = requests.post(api_servers, headers=headers).json()

# Select a random server
server = random.choice(response)['data']
api_stream = f"https://111movies.com/{static_path}/{server}"
response = requests.post(api_stream, headers=headers).json()

# Extract video URL
video_url = response['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")