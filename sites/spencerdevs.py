import re
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from urllib.parse import urlparse
from Crypto.Protocol.KDF import PBKDF2


'''
Supports:
https://spencerdevs.xyz/
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
base_url = 'https://spencerdevs.xyz/movie/533535'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Utility Functions
''' Binary to Base64 '''
def binlist_to_b64(raw_binary_list):
    b64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    return ''.join('=' if int(b,2)==64 else b64chars[int(b,2)] for b in raw_binary_list)

# Prepare API URL
tmdb_id = base_url.split('/')[-1]
server = "1"

# Get encrypted binary
response = requests.get(f'https://servers.spencerdevs.xyz/{server}/m/{tmdb_id}', headers=headers).json()
snoopdog = response.get('snoopdog')

# Map binary to Base64
raw_binary_list = re.split(r'\s+', snoopdog.strip())
encrypted_b64 = binlist_to_b64(raw_binary_list)
encrypted_bytes = base64.b64decode(encrypted_b64)

# Get encryption parameters
password = encrypted_bytes[0:32]
salt = encrypted_bytes[32:48]
iv = encrypted_bytes[48:64]
ciphertext = encrypted_bytes[64:]

# Derive AES-256 key using PBKDF2-HMAC-SHA512
derived_key = PBKDF2(password=password, salt=salt, dkLen=32, count=100000, hmac_hash_module=SHA512)

# Decrypt using AES cipher (CBC mode)
cipher = AES.new(derived_key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ciphertext)

# Remove PKCS#7 padding
pad_len = plaintext[-1]
plaintext = plaintext[:-pad_len]
decrypted_data = plaintext.decode('utf-8')

# Extract video URL
video_url = decrypted_data

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")