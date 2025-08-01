import re
import time
import json
import html
import base64
import requests
from Crypto.Hash import SHA1
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from urllib.parse import urlparse, parse_qs

''' A Scraper module for KickAssAnime '''

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
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
key = "e13d38099bf562e8b9851a652d2043d3".encode('utf-8')
timestamp = int(time.time()) + 60

# Utilities
def get_domain(url):
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
    return domain

# Fetch page content
def real_extract(url):
    # Initialize required configs
    headers = {
        "Accept": "*/*",
        "Referer": get_domain(url),
        "User-Agent": user_agent
    }
    
    # Fetch initial page
    response = requests.get(url, headers=headers).text
    
    # Get Client Id and other infos
    client_id = re.search(r"cid:\s*\'(.*?)\'", response).group(1)
    client_info = bytes.fromhex(client_id).decode('utf-8').split('|')
    player_path = client_info[1].replace('player', 'source')
    query = parse_qs(urlparse(url).query).get("id")[0]
    
    # Create a SHA-1 Signature
    sign_str = ''.join([client_info[0], headers['User-Agent'], player_path, query, str(timestamp), key.decode('utf-8')])
    sign_hash = SHA1.new()
    sign_hash.update(sign_str.encode('utf-8'))
    signature = sign_hash.hexdigest()
    
    # Get encrypted data response
    source_url = f'{get_domain(url)}{player_path}?id={query}&e={timestamp}&s={signature}'
    response = requests.get(source_url, headers=headers).json()['data']
    
    # Get encrypted data and IV
    encrypted_data = base64.b64decode(response.split(':')[0])
    iv = bytes.fromhex(response.split(':')[1])
    
    # Decrypt encrypted data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = cipher.decrypt(encrypted_data)
    decrypted_data = unpad(decrypted_bytes, AES.block_size).decode('utf-8')
    
    # Extract video URL
    json_data = json.loads(decrypted_data)
    video_url = json_data['hls']
    
    # Return video URL
    return f'https:{video_url}'