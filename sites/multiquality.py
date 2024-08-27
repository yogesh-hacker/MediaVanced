import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import re
import json 
import json
import base64
import codecs

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def save_file_in_internal_directory(filename, content, directory='/storage/emulated/0'):
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File saved to {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
    

default_domain = "https://swift.multiquality.click"
initial_headers = {
    'Referer': default_domain,
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}
print(f"\n{Colors.OKCYAN}TARGET: {default_domain}{Colors.ENDC}")

cookies = {
    'ui': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MjAzNTgxMjQsIm5iZiI6MTcyMDM1ODEyNCwiZXhwIjoxNzUxNDYyMTQ0LCJkYXRhIjp7InVpZCI6NDU0MDA0LCJ0b2tlbiI6IjdjNmMwMzEzYThhOGUzOTczNGZjMDI2MDQ2Y2JlNzkzIn19.LXWUfS004XLU6irNvIiNbxmG0weQ-mjZr7rzUhQdBjk'
}

proxy = {
    "http": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128",
    "https": "http://qvgxntjn:1cyxq9jfd6rh@45.127.248.127:5128"
}

base_url = "https://swift.multiquality.click/embed/10sv3SOApEbQvb0"
session = requests.Session()

def decodeSalt(e):
    t = ""
    for c in e:
        t += str(ord(c) - 100)
    return t

initial_response = session.get(base_url, headers=initial_headers)
html_content = initial_response.text

# Extract and evaluate the code
code = re.findall(r'_juicycodes\(([^\)]+)', html_content, re.IGNORECASE)[0]
code = eval(code)

# Process the salt and the obfuscated JavaScript code
salt = ''.join([str(ord(char) - 100) for char in code[-3:]])
encoded_js = code[:-3]
padding_len = (len(encoded_js) + 3) % 4
encoded_js += "==="[:-padding_len]
encoded_js = encoded_js.replace("_", "+").replace("-", "/")

# Base64 decode and then ROT13 decode the result
decoded_js = codecs.decode(codecs.decode(encoded_js.encode('ascii'), 'base64').decode('ascii'), 'rot13')

# Map symbols to their corresponding index values and process them
symbol_map = ["`", "%", "-", "+", "*", "$", "!", "_", "^", "="]
index_string = ''.join([str(symbol_map.index(char)) for char in decoded_js])

# Split the index_string into chunks of 4 characters each
splitted_index = [index_string[i:i + 4] for i in range(0, len(index_string), 4)]

# Decode each chunk back to characters
final_string = ""
for c in splitted_index:
    decoded_char = int(c) % 1000 - int(salt)
    final_string += chr(decoded_char)

# Replace escaped forward slashes with normal slashes in a string
normal_string = final_string.replace(r'\/', '/')

# Regex to find the file URL
regex = r'"file":"(https:\/\/[^"]+\.m3u8)"'

# Find all matches
url = re.search(regex, normal_string).group(1)

regex = r'"ping":"([^"]+)"'

# Find all matches
ping_url = default_domain+re.search(regex, html_content).group(1).replace(r'\/', '/')
regex = r'"token":"([^"]+)"'
token = re.search(regex, html_content).group(1).replace(r'\/', '/')

data = {
    "_token": token,
    "__type": "dawn",
    "pingID": "821ba6b35ee100737b8eddf3ce4bab9f"
}

initial_headers = {
    'Referer': base_url,
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Dest': 'empty',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
}

print("\n######################")
print("######################")
print(f"Captured URL: {Colors.OKGREEN}{url}{Colors.ENDC}")
print("######################")
print("######################\n")
print(f"\n{Colors.WARNING}###Sorry but I dont know how to play this URL, If you know please send msg!")