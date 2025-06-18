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
    "Content-Type": "application/font-woff2",
    "X-Requested-With":"XMLHttpRequest",
    "X-Csrf-Token":"HXUwCQsIHigJ7tveUt7toXQysUmtvLp3"
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input_bytes):
    source_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    target_chars = "ijdwDIx49zeGg3BnpNEJSh_kb8f5KHcyuZPrRXaC1QUsV0v-lLTWoY26FA7qtMOm"
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
key_hex = "023061be4ba16814ba0a3628b99470931b7d291ca3c8d3cf8030fee995d9b70c"
iv_hex = "3cb95c4d6701fc03a723c35045d6464d"
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data)

# XOR operation
xor_key = bytes.fromhex("b0660a2812a851")
xor_result = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(aes_encrypted))

# Custom encoded string
encoded_final = custom_encode(xor_result)

# Make final request
static_path = "/8dd52148-bacc-55b8-a4c7-9237d0cd651b/bd3414ce7337186ad8f29166ebd287262844fb44/APA91S69lxkcphkoOMhy2G14PsF6FJ_E0WpL7ivuCbSlY6uQymWo4AosiXUD63BFrrCIZzhB0MFV0v2szrqZhD0TmSeNuXJQPDCqYHJIOZJA_zQZETb3s7GbrJxPWqejxtg7si3iZ4l3_qNCJrMG-Iv8p4bG7zyQrTu0heRD_MyaJ_2Z6SI0im6/33b7fb6e/osavecgav/1000069821241725/b62512fdeff941714d00e6bb5ea55b543572cf2775f2d313163fbdbf910f5fc2/l"
data = {}
api_servers = f"https://vidfast.pro{static_path}/MOUJHVybOkLOGA/{encoded_final}"
response = session.post(api_servers, headers=headers, json=data).json()

# Select a random server
server = random.choice(response)['data']
api_stream = f"https://vidfast.pro/{static_path}/ZwU/{server}"
response = requests.post(api_stream, headers=headers).json()

# Extract video URL
video_url = response['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")