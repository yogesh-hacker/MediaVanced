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

# Haha @Cinemaos, bro… after a decade, I was busy with my life, Welcome Me Now! 😉

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
base_url = "https://cinemaos.live/movie/watch/1272837"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
primary_hmac_key = "a7f3b9c2e8d4f1a6b5c9e2d7f4a8b3c6e1d9f7a4b2c8e5d3f9a6b4c1e7d2f8a5"
secondary_hmac_key = "d3f8a5b2c9e6d1f7a4b8c5e2d9f3a6b1c7e4d8f2a9b5c3e7d4f1a8b6c2e9d5f3"
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

# Get content info
match = re.search(r'\/cinemaos.live\/(.*?)\/watch\/(\d+)(?:\?season=(\d+)&episode=(\d+))?', base_url)
if match:
    content_type = match.group(1)
    content_id, season, episode = (
        match.group(2),
        match.group(3) or None,
        match.group(4) or None
    )

# Get IMDB ID of the content
response = requests.get(f"https://api.themoviedb.org/3/{content_type}/{content_id}?api_key={api_key}&append_to_response=external_ids").json()
imdb_id = response.get('imdb_id') or (response.get('external_ids') or {}).get('imdb_id')

# Construct the message string
message = f"tmdbId:{content_id}|imdbId:{imdb_id}"
if season and episode:
    message += f"|seasonId:{season}|episodeId:{episode}"

# Get the secret token for request
primary_secret = hmac.new(primary_hmac_key.encode(), message.encode(), hashlib.sha256).hexdigest()
final_secret = hmac.new(secondary_hmac_key.encode(), primary_secret.encode(), hashlib.sha256).hexdigest()

# Get encrypted data
response = requests.get(f"{default_domain}/api/providerv2?type={content_type}&tmdbId={content_id}&imdbId={imdb_id}&seasonId={season}&episodeId={episode}&t=&ry=&secret={final_secret}", headers=headers).json()
decryption_parameters = response.get('data')

# Extract hex strings from the response
encrypted_hex = decryption_parameters.get('encrypted')
iv_hex = decryption_parameters.get('cin')
auth_tag_hex = decryption_parameters.get('mao')
salt_hex = decryption_parameters.get('salt')

# Convert the password and all hex-encoded values into bytes
password = b"a1b2c3d4e4f6477658455678901477567890abcdef1234567890abcdef123456"
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
streaming_data = json.loads(decrypted_data).get('sources')
valid_entries = [v for v in streaming_data.values() if isinstance(v, dict) and 'url' in v]
random_choice = random.choice(valid_entries)
video_url = random_choice.get('url')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print(f"{Colors.okcyan}User-Agent:{Colors.endc} {user_agent}")
print("\n")
