import re
import json
import time
import requests
from urllib.parse import urlparse
import catplayer
import vidstreaming

'''
Supports:
https://krussdomi.com/
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
base_url = 'https://krussdomi.com/vidstreaming/player.php?id=688bc586169c31976b031b07&ln=zh-CN'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Origin': default_domain,
    'Referer': default_domain,
    'User-Agent': user_agent
}


if 'cat-player' in base_url:
    video_url = catplayer.real_extract(base_url)
elif 'vidstreaming' in base_url: 
    video_url = vidstreaming.real_extract(base_url)
else:
    video_url = None

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")