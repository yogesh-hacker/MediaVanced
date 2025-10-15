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
https://vidfast.pro/
'''

# @Vidfast, Have a nice Day!

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
    "X-Requested-With": "XMLHttpRequest"
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input_bytes):
    source_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    target_chars = "qKSV9YJhF-WvABcOTH6P1ewt8NrfkREg3LZjU2b_GnmyaDI5piX7xz0CoMuQdl4s"
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
key_hex = '3d57e7fcb67c95d0cffa215230aa1cbbd18421a448305a51f4d4505a1fd1305f'
iv_hex = '5799f00dfd2f5dfecd20880567fdf7fa'
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

# Encrypt raw data
cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data)

# XOR operation
xor_key = bytes.fromhex("ff094f1e808cd09a7c")
xor_result = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(aes_encrypted))

# Encode XORed data
encoded_final = custom_encode(xor_result)

# Get streaming servers
static_path = "hezushon/b09fcca4f7144731f91e8ef917d2ace2ec6a29aa19a199b12a9d02d132db0ee9/kirumo/11bec683-3937-5830-b400-1ba5ab45241f/wuf/s/APA91e_LxHlKO3YiQ7vznjtYzGy69DCoEINphFQr51qaVRBjehCSbP1Xz9Ks0M503tPCX73Uei4u-LG_yOezROuHI-X_YXeNMLeRlbzyxYQDz9GLDQzeF5H0wBeo7IJ9IFGDho7KIbw_yM8V5JAgcnB-SgNUzWVbgX0UPKWlHmpAlTn7f1TvIoB/143b6797/1000019772292744"
data = {}
api_servers = f"https://vidfast.pro/{static_path}/5_5N/{encoded_final}"
response = scraper.get(api_servers).json()

# Select a random server
server = random.choice(response)['data']
api_stream = f"https://vidfast.pro/{static_path}/kruiW6A/{server}"
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