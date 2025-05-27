import re
import execjs
import requests
from base64 import b64decode
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from Crypto.Cipher import ARC4

'''
Supports:
https://tatavid.com/
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
base_url = "https://tatavid.com/embed-jhwg9kjiibmo.html"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent
}

# Fetch initial page
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')

# Extract Encrypted Data
encrypted_data = soup.select_one('input#func')['value']
ciphertext = b64decode(encrypted_data)

# Decode encoded Js
encoded_script = next((s.string for s in soup.select('script') if s.string and "ﾟωﾟﾉ" in s.string), None)
js_code = """function aadecode(t){t = t.replace("\\) \\('_'\\)","");t = t.replace("\\(ﾟДﾟ\\) \\['_'\\] \\(","return ");var x = new Function(t);var r = x();return r;}"""
ctx = execjs.compile(js_code)
decoded_script = ctx.call("aadecode", encoded_script)

# Extract RC4 Key
key = re.search(r'=\s*\w+\(\'(.*?)\',', decoded_script).group(1)
key_bytes = key.encode()

# RC4 Decrypt
decipher = ARC4.new(key_bytes)
decrypted = decipher.decrypt(ciphertext)
decoded_data = decrypted.decode()

# Extract Video URL
video_url = re.search(r'\'src\',\s*\'(.*?)\'', decoded_data).group(1)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")