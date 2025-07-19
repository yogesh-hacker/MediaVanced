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
    "Content-Type": "text/plain",
    "X-Requested-With":"XMLHttpRequest",
    "X-CSRF-Token": "Y7DMqDbqlMjTDusCDO09jzaw6PJxLbTe"
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input_bytes):
    source_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    target_chars = "mGSQhJqxO3T54WaFH6v8Rt19X0KCn_el7rUwYAB-kzcIEdVNpDboPjMZiL2gyfsu"
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
key_hex = "5aa7329ee949901b0f5059836b7949e329e8de17aa47a40783e51befd6747634"
iv_hex = "b137ab832c1c137124d9977572db3456"
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data)

# XOR operation
xor_key = bytes.fromhex("25a053ff3760d94591")
xor_result = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(aes_encrypted))

# Custom encoded string
encoded_final = custom_encode(xor_result)

# Make final request
static_path = "8011da2784761fc40ac5b3d9ffb6562c124ed5ca/ni/etlagmo/b/5d427d47-a6f8-5a94-878b-382d85e863ee/c91394ea8a28601ae2718f2b548d9e91535ef725f363be0d011065e3b4611e72/1000084419912790/67e0420a"
data = {}
api_servers = f"https://vidfast.pro/{static_path}/4Zmitbs0MEEg5Q/{encoded_final}"
response = session.post(api_servers, headers=headers, json=data).json()

# Select a random server
server = random.choice(response)['data']
api_stream = f"https://vidfast.pro/{static_path}/4n5q/{server}"
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