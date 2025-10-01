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
charset = {
    "00000000": "A",
    "00000001": "B",
    "00000010": "C",
    "00000011": "D",
    "00000100": "E",
    "00000101": "F",
    "00000110": "G",
    "00000111": "H",
    "00001000": "I",
    "00001001": "J",
    "00001010": "K",
    "00001011": "L",
    "00001100": "M",
    "00001101": "N",
    "00001110": "O",
    "00001111": "P",
    "00010000": "Q",
    "00010001": "R",
    "00010010": "S",
    "00010011": "T",
    "00010100": "U",
    "00010101": "V",
    "00010110": "W",
    "00010111": "X",
    "00011000": "Y",
    "00011001": "Z",
    "00011010": "a",
    "00011011": "b",
    "00011100": "c",
    "00011101": "d",
    "00011110": "e",
    "00011111": "f",
    "00100000": "g",
    "00100001": "h",
    "00100010": "i",
    "00100011": "j",
    "00100100": "k",
    "00100101": "l",
    "00100110": "m",
    "00100111": "n",
    "00101000": "o",
    "00101001": "p",
    "00101010": "q",
    "00101011": "r",
    "00101100": "s",
    "00101101": "t",
    "00101110": "u",
    "00101111": "v",
    "00110000": "w",
    "00110001": "x",
    "00110010": "y",
    "00110011": "z",
    "00110100": "0",
    "00110101": "1",
    "00110110": "2",
    "00110111": "3",
    "00111000": "4",
    "00111001": "5",
    "00111010": "6",
    "00111011": "7",
    "00111100": "8",
    "00111101": "9",
    "00111110": "+",
    "00111111": "/",
    "01000000": "="
}

# Prepare API URL
tmdb_id = base_url.split('/')[-1]
server = "1"

# Get encrypted binary
response = requests.get(f'https://servers.spencerdevs.xyz/{server}/m/{tmdb_id}', headers=headers).json()
snoopdog = response.get('snoopdog')

# Map binary to Base64
raw_binary_list = re.split(r'\s+', snoopdog.strip())
encrypted_b64 = ''.join([charset.get(binary, '?') for binary in raw_binary_list])
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