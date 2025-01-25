import requests
import re
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib
import struct
import os

## Library v6.3 ##

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

'''
Message to Vidstream/Animedekho: Hello, developers! What are you guys up to? Your new method is no challenge—I’ve cracked it again. I’ve identified the pattern, and it’s ridiculously easy now. Next time, step up your game with better obfuscation and a more advanced approach. This is MediaVanced (Media Advanced), not a standard library like others. If I want, I can crack all your methods. It only took me 30 minutes to break it! Haha!
'''


# Configuration
base_url = "https://vidstreamnew.xyz/v/EDMfWZnXmaYU/"
headers = {
    'Referer': "https://vidstreamnew.xyz/",
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}


# Convert string to 32-bit word array
def string_to_32bit_words(text):
    words = [0] * ((len(text) + 3) // 4)
    for i, char in enumerate(text):
        words[i >> 2] |= (ord(char) & 255) << (24 - (i % 4) * 8)
    return words

# Convert byte array to 32-bit word array
def bytes_to_32bit_words(byte_data):
    words = []
    for i in range(0, len(byte_data), 4):
        word = 0
        for j in range(4):
            if i + j < len(byte_data):
                word |= byte_data[i + j] << (24 - j * 8)
        words.append(struct.unpack('>i', struct.pack('>I', word))[0])
    return words

# Derive key using PBKDF2
def derive_key(password, salt, key_size, iterations, hash_algo):
    password_bytes = b''.join(word.to_bytes(4, 'big') for word in password)
    salt_bytes = b''.join(word.to_bytes(4, 'big') for word in salt)
    return hashlib.pbkdf2_hmac(hash_algo, password_bytes, salt_bytes, iterations, dklen=key_size)

# Base64 and Hex parsers
hex_parser = lambda x: bytes.fromhex(x)
base64_parser = lambda x: base64.b64decode(x)


# Fetch and extract encrypted data
response = requests.get(base_url, headers=headers).text
encrypted_data_match = re.search(r"const\s+Encrypted\s*=\s*'(.*?)'", response)

if not encrypted_data_match:
    print("No encrypted data found.")
    exit()

encrypted_data = encrypted_data_match.group(1)

# Decode and parse JSON
decoded_data = base64.b64decode(encrypted_data).decode('utf-8')
parsed_json = json.loads(decoded_data)

# Derive key
salt = string_to_32bit_words(parsed_json['salt'])
password = string_to_32bit_words("3%.tjS0K@K9{9rTc")
derived_key = derive_key(password, salt, key_size=32, iterations=999, hash_algo='sha512')


# Prepare IV and data
iv = hex_parser(base64_parser(parsed_json['iv']).hex())
encrypted_content = base64_parser(parsed_json['data'])

# Decrypt data
cipher = AES.new(derived_key, AES.MODE_CBC, iv=iv)
decrypted_data = cipher.decrypt(encrypted_content)

# Unpad and print plaintext
final_result = ''
try:
    final_result = unpad(decrypted_data, AES.block_size).decode()
except ValueError as e:
    print("Padding Error:", e)

video_url_pattern = r'file:\s*"([^"]+)"'
video_url_match = re.search(video_url_pattern, final_result)

video_url = ""
if video_url_match:
    video_url = video_url_match.group(1)
else:
    print("No video URL found.")

print("######################")
print("######################")
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("######################")
print("######################")
print(f"{Colors.warning}### Please use the header \"Referer: https://vidstreamnew.xyz\" or the CDN host to access the URL, along with a User-Agent.\n")
