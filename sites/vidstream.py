import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, unquote
import re
import json
import base64
import zlib

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

base_url = "https://vidstreamnew.xyz/v/EDMfWZnXmaYU/"
default_domain = "https://vidstreamnew.xyz/"
request_headers = {
    'Referer': default_domain,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

print(f"\n{Colors.okcyan}TARGET: {default_domain}{Colors.endc}")

http_session = requests.Session()

initial_page_content = http_session.get(base_url, headers=request_headers).text

encrypted_data_pattern = r"const\s+Encrypted\s*=\s*'(.*?)'"
encrypted_data_match = re.search(encrypted_data_pattern, initial_page_content)

encrypted_data = ""
if encrypted_data_match:
    encrypted_data = encrypted_data_match.group(1)
else:
    print("No encrypted data found.")

decoded_bytes = base64.b64decode(encrypted_data)
decoded_characters = []

for byte in decoded_bytes:
    binary_representation = f'{byte:08b}'
    reversed_binary = binary_representation[::-1]
    reversed_integer = int(reversed_binary, 2)
    decoded_characters.append(reversed_integer)

byte_array = bytearray(decoded_characters)
decompressed_data = ""
try:
    decompressed_data = zlib.decompress(byte_array).decode('utf-8')
except zlib.error:
    print("The data is not a valid ZLIB compressed file.")
except Exception as e:
    print(f"An error occurred during decompression: {e}")

special_to_alphabet_map = {
    "!": "a", "@": "b", "#": "c", "$": "d", "%": "e",
    "^": "f", "&": "g", "*": "h", "(": "i", ")": "j"
}

processed_data = ''.join(special_to_alphabet_map.get(char, char) for char in decompressed_data)
decoded_base64_data = base64.b64decode(processed_data)

decoded_url = unquote(decoded_base64_data.decode('utf-8'))

video_url_pattern = r'file:\s*"([^"]+)"'
video_url_match = re.search(video_url_pattern, decoded_url)

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