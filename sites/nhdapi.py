import re
import requests
from urllib.parse import urlparse

'''
Supports:
https://nhdapi.xyz/
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
base_url = 'https://nhdapi.xyz/movie/666243'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Accept': '*/*',
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Get media path
media_path = base_url.replace('https://nhdapi.xyz/', '')

# Construct API URL
servers = ['flixhq', 'hollymoviehd']
api_url = f'https://server.nhdapi.xyz/{servers[0]}/{media_path}'

# Fetch streaming data
response = requests.get(api_url, headers=headers).json()

# Extract video URL
video_url = response.get('url')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in response.get('headers').items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")