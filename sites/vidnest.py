import re
import os
import time
import random
import requests
from urllib.parse import urlparse

'''
Supports:
https://vidnest.fun/
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
base_url = 'https://vidnest.fun/tv/94605/1/1'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
passphrase = 'A7kP9mQeXU2BWcD4fRZV+Sg8yN0/M5tLbC1HJQwYe6pOKFaE3vTnPZsRuYdVmLq2'
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Pick a random server and get ID
servers = ['allmovies', 'hollymoviehd']
server = random.choice(servers)

# Get item id
media_type = 'movie'
if 'tv' in base_url:
    media_type = 'tv'
    item_id = base_url.split('/tv/')[-1]
else:
    item_id = base_url.split('/movie/')[-1]

# Fetch encrypted streams
response = requests.get(f'https://new.vidnest.fun/{server}/{media_type}/{item_id}', headers=headers).json()
encrypted = response.get('data')

# Prepare payload
timestamp = int(time.time())
random_iv = os.urandom(16).hex()
payload = {
    'data': encrypted,
    'timestamp': timestamp,
    'nonce': random_iv
}

# Decrypt data from server
response = requests.post('https://new.vidnest.fun/decrypt', headers=headers, json=payload).json().get('data')

# Get sources or streams
streaming_data = response.get('sources') or response.get('streams')

# Extract video URL
random_choice = random.choice(streaming_data)
video_url = random_choice.get('file') or random_choice.get('url')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print("\n")
