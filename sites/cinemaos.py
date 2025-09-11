import re
import json
import hmac
import random
import base64
import hashlib
import requests
from Crypto.Cipher import AES
from urllib.parse import urlparse
from Crypto.Util.Padding import unpad

'''
Supports:
https://cinemaos.live/
'''

# @Cinemaos, Why making it complex? Signature, AES & Auth. What about latency?

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
base_url = "https://cinemaos.live/movie/watch/1061474"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
secret_key = "a1b2c3d4e4f6589012345678901477567890abcdef1234567890abcdef123456"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
headers = {
    "Origin": default_domain,
    "Referer": default_domain,
    "User-Agent": user_agent,
}

# Get auth token
auth_api = f'{default_domain}/api/auth/securex'
response = requests.get(auth_api, headers=headers).json()
auth_token = requests.post(auth_api, headers=headers, json=response).json()['token']
headers['Authorization'] = f'Bearer {auth_token}'

# TMDB API Key (VidRock)
''' ⚠️ Warning: Unauthorized use of another person’s API key is prohibited. The provided key is intended strictly for testing purposes. We strongly recommend generating and using your own API key in production.'''
api_key = base64.b64decode("NTRlMDA0NjZhMDk2NzZkZjU3YmE1MWM0Y2EzMGIxYTY=").decode('utf-8')

# Get required data
if 'movie' in base_url:
    data_id = base_url.split('/')[-1]
    response = requests.get(f"https://api.themoviedb.org/3/movie/{data_id}?api_key={api_key}").json()
    release_year = response['release_date'].split('-')[0]
    title = response['title']
    imdb_id = response['imdb_id']
else:
    exit(print(f'{Colors.fail}TV Series currently not supported!'))

# Construct the message string to be signed
tmdb_id = data_id
season_id = ""
episode_id = ""
message_string = f"tmdb:{tmdb_id}|season:{season_id}|episode:{episode_id}"

# Generate an HMAC-SHA256 signature for the media identifiers using a secret key
hmac_signature = hmac.new(secret_key.encode("utf-8"), message_string.encode("utf-8"), hashlib.sha256)
signature_hash = hmac_signature.hexdigest()

# Get encrypted data
response = requests.get(f"{default_domain}/api/cinemaos?type=movie&tmdbId={data_id}&imdbId={imdb_id}&t={title}&ry={release_year}&secret={signature_hash}", headers=headers).json()['data']

# Extract hex strings from the response
encrypted_hex = response['encrypted']
iv_hex = response['cin']
auth_tag_hex = response['mao']

# Convert Hex to Bytes
key_hex = "a1b2c3d4e4f6589012345678901477567890abcdef1234567890abcdef123456"
key = bytes.fromhex(key_hex)
ciphertext = bytes.fromhex(encrypted_hex)
iv = bytes.fromhex(iv_hex)
auth_tag = bytes.fromhex(auth_tag_hex)

# Decrypt using AES-256-GCM
cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
cipher.update(b'') # AAD
cipher.digest_size = 16
decrypted_data = cipher.decrypt(ciphertext).decode('utf-8')
cipher.verify(auth_tag)

# Extract video URL
json_data = json.loads(decrypted_data)['sources']
valid_entries = [v for v in json_data.values() if isinstance(v, dict) and 'url' in v]
random_choice = random.choice(valid_entries)
video_url = random_choice['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print(f"{Colors.okcyan}User-Agent:{Colors.endc} {user_agent}")
print("\n")