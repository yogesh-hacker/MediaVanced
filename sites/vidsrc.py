import re
import json
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from urllib.parse import urlparse
from Crypto.Util.Padding import pad

'''
Supports:
https://vidsrc.cc/
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
base_url = "https://vidsrc.cc/v2/embed/movie/385687?autoPlay=false"
api_url = "https://vidsrc.cc/api" 
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "User-Agent": user_agent,
}

# Utility Functions
''' Encrypts Movie ID and User ID '''
def generate_vrf(movie_id: str, user_id: str) -> str:
    key = SHA256.new(user_id.encode()).digest()
    iv = bytes(16)

    plaintext = pad(movie_id.encode(), AES.block_size)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext)

    encoded = base64.b64encode(ciphertext).decode()
    url_safe = encoded.replace('+', '-').replace('/', '_').replace('=', '')

    return url_safe

# Fetch Initial Response
response = requests.get(base_url, headers=headers).text

# Extract all key-value pairs from the response
pattern = r'var\s+(\w+)\s*=\s*"([^"]*)"'
matches = re.findall(pattern, response)

# Convert the matches into a dictionary for easy access
data = {key: value for key, value in matches}

# Retrieve required fields from the extracted data
movie_id = data.get('movieId')
imdb_id = data.get('imdbId')
user_id = data.get('userId')
content_type = data.get('movieType')
version = data.get('v')
verification_token = generate_vrf(movie_id, user_id)

# Get all servers
api_servers = f'{api_url}/{movie_id}/servers?id={movie_id}&type={content_type}&v={version}&vrf={verification_token}&imdbId={imdb_id}'
response = requests.get(api_servers, headers=headers).json()

# Retrieve iframe URLs for each server
iframe_urls = []

for server in response['data']:
    server_hash = server.get('hash')
    server_name = server.get('name')

    iframe_endpoint = f"{api_url}/source/{server_hash}"
    iframe_response = requests.get(iframe_endpoint, headers=headers).json()

    if iframe_response.get('success'):
        source_url = iframe_response.get('data', {}).get('source')
        iframe_urls.append({server_name: source_url})

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print("Captured Providers:")
for iframe in iframe_urls:
    provider_name, source_url = next(iter(iframe.items()))
    print(f"{Colors.okcyan}{provider_name}: {Colors.okgreen}{source_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
