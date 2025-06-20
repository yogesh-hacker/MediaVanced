import re
import random
import base64
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import pad

'''
Supports:
https://vidfast.pro/
'''

# @Vidfast, Don't try to challenge. :}

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
base_url = "https://vidfast.pro/movie/533535"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Accept": "*/*",
    "Referer": default_domain,
    "User-Agent": user_agent,
    "x-session": "",
    "X-Requested-With":"XMLHttpRequest",
    "X-Csrf-Token":"lVx7BVtk9c3SMNbF49PNvUc7GV5zzdem"
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input_bytes):
    source_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    target_chars = "Ju9Egn27FZNe-kaMUtOBAmf0qp3xDYlTX6PhiL5SRjzQIsHvoVw_WC4dGc1Ky8rb"
    translation_table = str.maketrans(source_chars, target_chars)

    encoded = base64.urlsafe_b64encode(input_bytes).decode().rstrip('=')
    
    return encoded.translate(translation_table)

session = requests.Session()

# Fetch page content
response = session.get(base_url, headers=headers).text

# Extract raw data
match = re.search(r'\\"en\\":\\"(.*?)\\"', response)
if not match:
    exit(print("No data found!"))
raw_data = match.group(1)

# AES encryption setup
key_hex = "13346e2c05211f72e46a465e953fd5410826715e28d927f92ea5f4daee985c8b"
iv_hex = "b83bcd42b90f5364e9b95c398264bca4"
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data)

# XOR operation
xor_key = bytes.fromhex("3fc3e051ddc9dd8a74")
xor_result = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(aes_encrypted))

# Custom encoded string
encoded_final = custom_encode(xor_result)

# Make final request
static_path = "/rebivol/ad/w/2c7998b18129848378021254f87db35df8f562b2/2cf30a7c/APA91nNHHa3xbnvasl8ciswLATkt2fIiVFciF5RLarK4oR7nrTpEDSBjO_kRoBJD730BWfo6bQZIpxCr-PAlSGc8GAAxueegNH5gNzrcqhPDliciuUDv0GTqb_2t1ik9pIAXpVaZ8inm6ey56Qf44wrOOPUfZYlkKuKs18mNKqBluBYTB5lBXWF/775d49bf3b9b4d082f5156cd9f36e21d42014547cd9282b1fe62ccbe3d09f66b/1000094661747536"
data = {}
api_servers = f"https://vidfast.pro{static_path}/k33a7dwPZst1/{encoded_final}"
response = session.post(api_servers, headers=headers, json=data).json()

# Select a random server
server = random.choice(response)['data']
api_stream = f"https://vidfast.pro/{static_path}/p6PWA5s/{server}"
response = requests.post(api_stream, headers=headers).json()

# Extract video URL
video_url = response['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")