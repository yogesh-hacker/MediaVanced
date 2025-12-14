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
    "X-Csrf-Token": "V8mmyuaJMUuox6S6Y8OVt5fdfQOyiZfQ",
    "X-Requested-With": "XMLHttpRequest"
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input_bytes):
    source_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    target_chars = "ki1GNs4Udpf5njK3B_ugAWCZxhtLmFaYIrHzoylP8JRSE-2DO6Qeb0vTMc7wVqX9"
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
key_hex = '8528c3493aa7eb34eb3894cb61cab170abbb624e784231bdf356545099fd5ceb'
iv_hex = '0763e69cce730974efaef9850c1740ac'
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

# Encrypt raw data
cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data)

# XOR operation
xor_key = bytes.fromhex("7bf1e94bf5b5a8c4b0e9")
xor_result = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(aes_encrypted))

# Encode XORed data
encoded_final = custom_encode(xor_result)

# Get streaming servers
static_path = "hezushon/ge/APA91xl1NnI4xc8CtapVcp2zqcOcEHjgs5yvQTObRg8wp8g4IpPT-DOUSyUlYmelXx_6N8Aku5I_pKSFtcPD4lmSTI6e4uutm4k0GlS9BCRw_euZhCua0o7HLiGUpXJcLDnO4IT1bSBc_Qtg7X0MUt5cC8puKswXqqnkUITa6r1srLMxCIMjT6m/390386d6-a716-5a65-a9cf-b6b268dc87af/1000028577337190/43d36190/8f97ec78acaf6a95ee303b5f6567ddf5df617d066f3416242e381753c9897057/gol/e"
data = {}
api_servers = f"https://vidfast.pro/{static_path}/d6MF/{encoded_final}"
response = scraper.get(api_servers).json()

# Select a random server
server = random.choice(response)['data']
api_stream = f"https://vidfast.pro/{static_path}/HYaF/{server}"
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