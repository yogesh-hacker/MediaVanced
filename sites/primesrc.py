import re
import json
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import unpad

'''
Supports:
https://primesrc.me/
https://primesrc.click/
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
base_url = 'https://primesrc.me/embed/movie?imdb=tt0110357'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
aes_key = b"kiemtienmua911ca"
aes_iv  = b"1234567890oiuytr"
default_domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Get content info
match = re.search(r'embed\/(.*?)\?\w+=(tt\d+)', base_url)
if match:
    content_type = match.group(1)
    content_id = match.group(2)

# Get servers list
response = requests.get(f'{default_domain}/api/v1/s?imdb={content_id}&type={content_type}').json()
servers = response.get('servers')
server_key = servers[0].get('key')

# Get server ID
response = requests.get(f'{default_domain}/api/v1/l?key={server_key}').json()
server_url = response.get('link')
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(server_url))
server_id = server_url.split('#')[1]

# Get streaming info
response = requests.get(f'{default_domain}/api/v1/video?id={server_id}', headers=headers).text
encrypted_bytes = bytes.fromhex(response)

# Decrypt using AES-256-CBC 
cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
decrypted_bytes = cipher.decrypt(encrypted_bytes)

# Get decrypted plaintext
plaintext = unpad(decrypted_bytes, AES.block_size).decode('utf-8')
unescaped = plaintext.replace('\\', '')

# Extract video URL
video_url = re.search(r'\"source\":\"(.*?)\"', unescaped).group(1)

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)

# Print headers
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print(f"{Colors.okcyan}User-Agent:{Colors.endc} {user_agent}")
print("\n")