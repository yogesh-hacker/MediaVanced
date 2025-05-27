import re
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
    dst = "FqpVQOUW9yascEh47TYu6r8NgfGmtHKPiI-eJvBZLwS2b3ndCjzDAlxXkRMo05_1"
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
key_hex = "68fa4221681cf65607a1d5182935ad661cdbd31e9e6fabc2a177346e058f3826"
iv_hex = "0508b5543bece4f350082411b772213e"
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data).hex()

# XOR operation
xor_key = bytes.fromhex("616c438ff0e2")
xor_result = ''.join(chr(ord(char) ^ xor_key[i % len(xor_key)]) for i, char in enumerate(aes_encrypted))

# Custom encoded string
encoded_final = custom_encode(xor_result)

# Make final request
static_path = "8e39ee3bc9096d8b2182b11bb3408ecb2d49d6ea/63f9b2f13d6e49d5626f55ad4dd073eb44c855576623c445f9297dbc41aca8d2/APA91pnnfHpSk-JUXVYqNM-8uZFTnjnkimXJeWy3y8wFIOoGQUuQ0T3ec_a5VZh6g4K0J8VjDJOoGWa3mBbrkq8ktvEu-YBcGVOHOxSQc5AGxcb2HDHjY0zAeBW5PXU54znsUHSteIQBYogeieO2qhWHircRCQAVAACZCfHwPNk0GrGiWEnpC67/1000085286633646/itailige"
api_url = f"https://111movies.com/{static_path}/{encoded_final}"
response = requests.post(api_url, headers=headers).json()

# Extract video URL
video_url = response['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")