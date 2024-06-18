import requests
import re
import os
from bs4 import BeautifulSoup
from pathlib import Path
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad
import json
from js2py import EvalJs


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


def pad_key(key):
    # Use SHA-256 to ensure key is 16 bytes long (AES-128)
    hash_obj = SHA256.new()
    hash_obj.update(key.encode('utf-8'))
    return hash_obj.digest()[:16]


default_domain = "https://vidstreamnew.xyz/"
print(f"\n{Colors.OKCYAN}TARGET: {default_domain} {Colors.ENDC}")
session = requests.Session()

initial_headers = {
    "Referer": default_domain,
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
}

base_url = "https://vidstreamnew.xyz/v/PjrmR68FunxF/"
initial_response = requests.get(base_url, headers=initial_headers)
initial_page_html = initial_response.text

pattern = r'JScripts = \'(.*)\''
matcher = re.search(pattern, initial_page_html)

if matcher:
    json_data = json.loads(matcher.group(1))

    ct = base64.b64decode(json_data['ct'])
    iv = bytes.fromhex(json_data['iv'])
    salt = bytes.fromhex(json_data['s'])

    assert len(iv) == 16, "IV must be 16 bytes long"

    pass_phrase = b"KB3c1lgTx6cHL3W"
    print(f'\n\n{Colors.OKCYAN}Using Password: {pass_phrase}{Colors.ENDC}')

    md = hashlib.md5()
    md.update(pass_phrase)
    md.update(salt)
    cache0 = md.digest()

    md = hashlib.md5()
    md.update(cache0)
    md.update(pass_phrase)
    md.update(salt)
    cache1 = md.digest()
    key = cache0 + cache1

    assert len(ct) % 16 == 0, "Ciphertext length must be a multiple of 16 bytes"

    cipher = AES.new(key, AES.MODE_CBC, iv)
    result = cipher.decrypt(ct)

    try:
        decrypted_plaintext = unpad(result, AES.block_size)
        javascript = json.loads(decrypted_plaintext)
        pattern = r'\"file\":\"(https?:\/\/[^\"]+)\"'
        matcher = re.search(pattern, javascript)

        if matcher:
            print("######################")
            print("######################")
            print(f"Captured URL: {Colors.OKGREEN}{matcher.group(1)}{Colors.ENDC}")
            print("######################")
            print("######################\n")
            print(f"\n{Colors.WARNING}###Please use header Referer: {default_domain} and a valid User-Agent to access the url")
        else:
            print("No matching file URL found in decrypted JavaScript.")
    except ValueError as e:
        print("Error unpadding the decrypted plaintext:", e)
else:
    print("Pattern not found in initial HTML.")
