import re
import os
import json
import base64
import requests
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad


'''
Supports:
https://play.playkrx18.site/
https://krx18.com/
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
base_url = "https://play.playkrx18.site/play/64eb239251e83d17db4cb79a"
domain_api = "https://api-play-240924.playkrx18.site/api/tp1rd"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
headers = {
    "Referer": "https://play.playkrx18.site/",
    'Content-Type': 'application/x-www-form-urlencoded',
    "User-Agent": user_agent
}

# Utility Functions
''' CryptoJS like AES-CBC encryption '''
def aes_encrypt(plaintext: str, password: str) -> str:
    salt = os.urandom(8)
    derived = b''
    while len(derived) < (32 + 16):
        last = derived[-16:]  # last IV block or empty
        md = MD5.new()
        md.update(last + password.encode('utf-8') + salt)
        derived += md.digest()
    key, iv = derived[:32], derived[32:48]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    encrypted = b"Salted__" + salt + ciphertext
    return base64.b64encode(encrypted).decode('utf-8')

''' CryptoJS like AES-CBC decryption '''
def aes_decrypt(ciphertext_b64: str, password: str) -> str:
    encrypted = base64.b64decode(ciphertext_b64)
    if not encrypted.startswith(b"Salted__"):
        raise ValueError("Invalid encrypted data format")
    
    salt = encrypted[8:16]
    ciphertext = encrypted[16:]

    derived = b''
    while len(derived) < (32 + 16):
        last = derived[-16:]  # last IV block or empty
        md = MD5.new()
        md.update(last + password.encode('utf-8') + salt)
        derived += md.digest()
    key, iv = derived[:32], derived[32:48]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)
    return plaintext.decode('utf-8')

''' Encrypts data to hex-encoded AES '''
def encrypt_hex_aes(plaintext, secret):
    base64_encrypted = aes_encrypt(plaintext, secret)
    return base64.b64decode(base64_encrypted).hex()

''' Decrypts hex-encoded AES data '''
def decrypt_hex_aes(hex_data, secret):
    data = base64.b64encode(bytes.fromhex(hex_data)).decode()
    return aes_decrypt(data, secret)

# Fetch Initial Response
response = requests.get(base_url, headers=headers).text

# Get encrypted File ID and User ID
matches = re.findall(r'const\s*id(?:User|file)_enc\s*=\s*"(.*?)"', response)
encrypted_file_id = matches[0]
encrypted_user_id = matches[1]

# Decrypt File ID and User ID
decrypted_file_id = decrypt_hex_aes(encrypted_file_id, "jcLycoRJT6OWjoWspgLMOZwS3aSS0lEn")
decrypted_user_id = decrypt_hex_aes(encrypted_user_id, "PZZ3J3LDbLT0GY7qSA5wW5vchqgpO36O");

# Post data
post_content = {
    'idfile': decrypted_file_id,
    'iduser': decrypted_user_id,
    'domain_play': 'https://my.9stream.net',
    'platform': 'Linux armv81',
    'hlsSupport': True,
    'jwplayer': {
        'Browser': {
            'androidNative': False,
            'chrome': True,
            'edge': False,
            'facebook': False,
            'firefox': False,
            'ie': False,
            'msie': False,
            'safari': False,
            'version': {
                'version': '137.0.0.0',
                'major': 137,
                'minor': 0
            }
        },
        'OS': {
            'android': True,
            'iOS': False,
            'mobile': True,
            'mac': False,
            'iPad': False,
            'iPhone': False,
            'windows': False,
            'tizen': False,
            'tizenApp': False,
            'version': {
                'version': '10',
                'major': 10,
                'minor': None
            }
        },
        'Features': {
            'iframe': False,
            'passiveEvents': True,
            'backgroundLoading': True
        }
    }
}

# Encrypt the content payload
encrypted_payload = encrypt_hex_aes(json.dumps(post_content), "vlVbUQhkOhoSfyteyzGeeDzU0BHoeTyZ")
signature = MD5.new((encrypted_payload + "KRWN3AdgmxEMcd2vLN1ju9qKe8Feco5h").encode('utf-8')).hexdigest()
post_data = {
    'data': f'{encrypted_payload}|{signature}'
}

# Make post Request and Decrypt Data
response = requests.post(f'{domain_api}/playiframe', headers=headers, data=post_data).json()
encrypted_data = response['data']

# Extract Video URL
video_url = decrypt_hex_aes(encrypted_data, "oJwmvmVBajMaRCTklxbfjavpQO7SZpsL")

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")