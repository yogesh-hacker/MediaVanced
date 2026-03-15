import re
import base64
import hashlib
import requests
import pyjson5 as json5
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import unpad

'''
Supports:
https://zencloudz.cc/
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
base_url = 'https://zencloudz.cc/e/g02b79b6edvh?v=2&a=1'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Utility Functions
'''Generate a simple substitution box (S-box) for key derivation'''
def generate_sbox(seed):
    sbox = bytearray(256)
    for index in range(256):
        sbox[index] = (index * 37 + seed) & 0xFF
    return sbox

'''Combine key fragments with XOR and S-box to derive the AES key'''
def derive_aes_key(key_fragment, secondary_key, dynamic_key, sbox):
    length = len(key_fragment)
    aes_key = bytearray(length)

    for i in range(length):
        aes_key[i] = key_fragment[i] ^ secondary_key[i] ^ dynamic_key[i] ^ sbox[i & 0xFF]

    return aes_key

# Fetch page content
response = requests.get(base_url, headers=headers).text

# Get site data
match = re.search(r'data:\s*\[null,null,(\{.*?\})\],\s*form:\snull', response)
site_data = json5.loads(match.group(1)).get('data')

# Get obfuscated data(s)
obfuscated_crypto_data = site_data.get('obfuscated_crypto_data')
obfuscation_seed = site_data.get('obfuscation_seed')

# Generate hashed seeds
seed_bytes = obfuscation_seed.encode('utf-8')
primary_seed_hash = hashlib.sha256(seed_bytes).hexdigest()

secondary_seed_bytes = primary_seed_hash.encode('utf-8')
secondary_seed_hash = hashlib.sha256(secondary_seed_bytes).hexdigest()

# Map dynamic field names
dynamic_fields = {
    "video_field": f"vf_{primary_seed_hash[0:8]}",
    "key_field": f"kf_{primary_seed_hash[8:16]}",
    "iv_field": f"ivf_{primary_seed_hash[16:24]}",
    "container_field": f"cd_{primary_seed_hash[24:32]}",
    "array_field": f"ad_{primary_seed_hash[32:40]}",
    "object_field": f"od_{primary_seed_hash[40:48]}",
    "token_field": f"{primary_seed_hash[48:64]}_{primary_seed_hash[56:64]}",
    "secondary_key_field": f"{secondary_seed_hash[0:16]}_{secondary_seed_hash[16:24]}"
}

# Extract key and IV from obfuscated crypto data
container_data = obfuscated_crypto_data.get(dynamic_fields["container_field"])
array_data = container_data.get(dynamic_fields["array_field"])
object_data = array_data[0].get(dynamic_fields["object_field"])

encrypted_key_b64 = object_data.get(dynamic_fields["key_field"])
iv_b64 = object_data.get(dynamic_fields["iv_field"])
secondary_key_b64 = site_data.get(dynamic_fields["secondary_key_field"])
token_reference = site_data.get(dynamic_fields["token_field"])

# Prepare Crypto Info
crypto_info = {
    "encrypted_key": encrypted_key_b64,
    "iv": iv_b64
}

# Fetch encrypted video data
token_response = requests.get(f'{default_domain}/api/m3u8/{token_reference}').json()
encrypted_video_b64 = token_response.get('video_b64')
dynamic_key_b64 = token_response.get('key_frag')

# Decode base64 components
encrypted_key_bytes = base64.b64decode(crypto_info["encrypted_key"])
secondary_key_bytes = base64.b64decode(secondary_key_b64)
dynamic_key_bytes = base64.b64decode(dynamic_key_b64)
iv_bytes = base64.b64decode(crypto_info["iv"])
ciphertext_bytes = base64.b64decode(encrypted_video_b64)

# Generate S-box seed and AES key ---
sbox_seed = int(obfuscation_seed[0:8], 16)
sbox_table = generate_sbox(sbox_seed)
aes_key = derive_aes_key(encrypted_key_bytes, secondary_key_bytes, dynamic_key_bytes, sbox_table)

# Decrypt AES-256-CBC
cipher = AES.new(aes_key, AES.MODE_CBC, iv_bytes)
plaintext_bytes = cipher.decrypt(ciphertext_bytes)
plaintext = unpad(plaintext_bytes, AES.block_size).decode()

# Extract video URL
video_url = plaintext

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")