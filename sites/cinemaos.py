import re
import json
import hmac
import random
import base64
import hashlib
import requests
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from urllib.parse import urlparse
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2

'''
Supports:
https://cinemaos.live/
'''

# Haha @Cinemaos, bro… cryptography is my playground now. PlayerX (scraper) made me unstoppable! 😉

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
secret_key = "a8f7e9c2d4b6a1f3e8c9d2b4a7f6e9c2d4b6a1f3e8c9d2b4a7f6e9c2d4b6a1f3"
parsed_url = urlparse(base_url)
default_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
headers = {
    "Origin": default_domain,
    "Referer": default_domain,
    "User-Agent": user_agent,
}

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
message_string = f"media|episodeId:{episode_id}|seasonId:{season_id}|tmdbId:{tmdb_id}"

# Generate an HMAC-SHA256 signature for the media identifiers using a secret key
hmac_signature = hmac.new(secret_key.encode("utf-8"), message_string.encode("utf-8"), hashlib.sha256)
signature_hash = hmac_signature.hexdigest()

# Get encrypted data
response = requests.get(f"{default_domain}/api/cinemaos?type=movie&tmdbId={data_id}&imdbId={imdb_id}&t={title}&ry={release_year}&secret={signature_hash}", headers=headers).json()['data']

# Extract hex strings from the response
encrypted_hex = response.get('encrypted')
iv_hex = response.get('cin')
auth_tag_hex = response.get('mao')
salt_hex = response.get('salt')

# Convert the password and all hex-encoded values into bytes
password = b"a1b2c3d4e4f6588658455678901477567890abcdef1234567890abcdef123456"
ciphertext = bytes.fromhex(encrypted_hex)
iv = bytes.fromhex(iv_hex)
auth_tag = bytes.fromhex(auth_tag_hex)
salt = bytes.fromhex(salt_hex)

# Derive a 256-bit AES key from the password and salt using PBKDF2 with SHA-256
key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)

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