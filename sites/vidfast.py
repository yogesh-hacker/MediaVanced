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
    "X-Csrf-Token": "JjcyiVDl4pPbnbSLUVDLiMFwJR8C2WNk",
    "X-Requested-With": "XMLHttpRequest",
}

# Utility Functions
''' Encodes input using Base64 with custom character mapping. '''
def custom_encode(input_bytes):
    source_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    target_chars = "ZYm5_ScNtbX3IgzV-7xk82BDR1aprAvWOhMwelUQ4iHdGuECTyF6os90fqPjLJnK"
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
key_hex = 'e30df70860e74df551ea7be6001a2baec9a38d3dc5d96b63830f8721098e1c53'
iv_hex = 'd04e83862d741774a4be0a60ebde5f89'
aes_key = bytes.fromhex(key_hex)
aes_iv = bytes.fromhex(iv_hex)

# Encrypt raw data
cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
padded_data = pad(raw_data.encode(), AES.block_size)
aes_encrypted = cipher.encrypt(padded_data)

# XOR operation
xor_key = bytes.fromhex("773e3c35d04495b4e9")
xor_result = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(aes_encrypted))

# Encode XORed data
encoded_final = custom_encode(xor_result)

# Get streaming servers
static_path = "hezushon/a/APA91PF9DMA4b5bJkuB33z2ZDGn2iCx2WLKkqD_P_Cxg4Km4ok_QhifhLIiI1Iot9obpDiXhYDQsrSypaRrTLy4j-rWowvM44fKIuJ8sXS20H7f-MgGjEUXiPIIP7SLbFCK93OIXj89ssW5r_N8QNchVUz7wLRltc8nYJIiFbvjJ0kQ6xSz6iny/1000085697207426/cek/ac7cdc69-3f2e-5d5f-82df-ca71bab8a274/b9de1beea88399820f70c22cd6827900c104af9daa5b526ce002f7847b550988/a94c1dc3d92a6cf9a1445d23d0f6c014a967562e"
data = {}
api_servers = f"https://vidfast.pro/{static_path}/SqhAfKdX/{encoded_final}"
response = scraper.get(api_servers).json()

# Select a random server
server = random.choice(response)['data']
api_stream = f"https://vidfast.pro/{static_path}/2z2p-GV3ow/{server}"
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