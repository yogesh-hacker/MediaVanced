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
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input_bytes):
    source_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    target_chars = "SlfpOi9DxzTcn683E2o7drBGCKW4XZFu0Q1MRtJbjykL_V-N5veAmHwaPqYhIsUg"
    translation_table = str.maketrans(source_chars, target_chars)
    encoded = base64.urlsafe_b64encode(input_bytes).decode().rstrip('=')
    return encoded.translate(translation_table)

# Fetch page content
response = requests.get(base_url, headers=headers).text

# Extract raw data
match = re.search(r'\\"en\\":\\"(.*?)\\"', response)
if not match:
    exit(print("No data found!"))
raw_data = match.group(1)

# AES encryption setup
key_hex = 'd9ff31a40dd415210c298a9d113a1963cf9c5253229a93709928788f12041f22'
iv_hex = 'e591e8af30972f444b5b3b206c60c598'
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

# Encrypt raw data
cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data)

# XOR operation
xor_key = bytes.fromhex("1261f48e150cbe")
xor_result = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(aes_encrypted))

# Encode XORed data
encoded_final = custom_encode(xor_result)

# Get streaming servers
static_path = "79198daa-820c-5b08-ae46-f7391a4cb4dc/APA91XB-tqjXq06x1tMAywlhBwZoXF6FQV1ytGGPiOlCKlVRNnQ5Gm9GfHEO62TBFQbKi9FmQxIsxYuEZDgVwV1nwEzvGANC19MEE7mz_0TKror9KYtgeLtoh4cJiuPV9IJCV-XV7R2A0F0CRzfQKqr--OLVvrDgspSOiGGJEVYHu6BqaLB7xes/4c12dad1e1340c2fa8d5df7a54e1afbdb55f8011/4a5bf14f8b528581e81c89a761a8068bd049c0f86219d9dba62335155f00e04b/sewlujom"
data = {}
api_servers = f"https://vidfast.pro/{static_path}/YDGUTEY/{encoded_final}"
response = requests.post(api_servers, headers=headers, json=data).json()

# Select a random server
server = random.choice(response)['data']
api_stream = f"https://vidfast.pro/{static_path}/xo8XtbY-sVen/{server}"
response = requests.post(api_stream, headers=headers).json()

# Extract video URL
video_url = response['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")