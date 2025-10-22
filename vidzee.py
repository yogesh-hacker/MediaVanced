import re
import base64
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import unpad

'''
Supports:
https://player.vidzee.wtf/
https://vidzee.wtf/
'''

# @Vidzee, I'm straight, may I show you?
# Gawk! Gawk! Gawk!

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
base_url = 'https://player.vidzee.wtf/embed/tv/1399/1/1'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
key_hex = '6966796f75736372617065796f75617265676179000000000000000000000000' # Do not decode :)
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Get content type and TMDB ID
media_type = 'movie' if 'movie' in base_url else 'tv'
server = 1 # Default

# Get tmdbId, season and episode
match = re.search(r'/(\d+)(?:/(\d+)/(\d+))?', base_url)
if media_type == "movie":
    media_id = match.group(1)
else:
    media_id = match.group(1)
    season = match.group(2)
    episode = match.group(3)

# Construct API URL
if media_type == 'movie':
    api_url = f'https://player.vidzee.wtf/api/server?id={media_id}&sr={server}'
else:
    api_url = f'https://player.vidzee.wtf/api/server?id={media_id}&sr={server}&ss={season}&ep={episode}'

# Get encrypted streaming URL
response = requests.get(api_url, headers=headers).json()
encrypted_url = response.get('url')[0].get('link')

# Decode decryption parameters
decoded = base64.b64decode(encrypted_url).decode()
iv_b64, ciphertext_b64 = decoded.split(':', 1)

# Prepare decryption parameters
iv = base64.b64decode(iv_b64)
ciphertext = base64.b64decode(ciphertext_b64)
key = bytes.fromhex(key_hex)

# Decrypt using AES-CBC
cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted_data = cipher.decrypt(ciphertext)

# Remove PKCS7 padding
plaintext_bytes = unpad(decrypted_data, AES.block_size)

# Extract video URL
video_url = plaintext_bytes.decode('utf-8')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")