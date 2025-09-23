import re
import os
import json
import time
import base64
import string
import random
import hashlib
import requests
from urllib.parse import urlparse

'''
Supports:
https://hexa.watch/
'''

# @Hexa – what did you think? That I’d never crack it again?  
# Hah! :) The demand for this scraper has skyrocketed,  
# so I’m carrying on the legacy! Hahaha!

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
base_url = "https://hexa.watch/watch/movie/1087192"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "Accept": "*/*",
    "User-Agent": user_agent
}

# Get Media ID and Type
media_type = 'movie' if 'movie' in base_url else 'tv'
match = re.search(r'/(\d+)(?:/(\d+)/(\d+))?', base_url)
media_id = f"{match.group(1)}/{match.group(2)}/{match.group(3)}" if media_type == "tv" else match.group(1)

# Support limited to movies for now
if media_type != 'movie':
    exit(f"{Colors.fail}Series are not supported by the API at the moment. Please wait for upcoming updates.{Colors.endc}")

# Get streaming data
'''
Due to the site's use of WASM, the decryption logic
and WASM implementation are hosted server-side.  
If you need the implementation script, reach out to me
on Discord (peerless_x).  
I am unable to make it publicly available.
'''
response = requests.get(f"https://hexa.yogesh-hacker.deno.net/?tmdbId={media_id}").json()
decrypted_data = response.get('sources').get('sources')

# Extract video URL
video_url = random.choice(decrypted_data)['url']

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")
print(f"{Colors.okcyan}Referer:{Colors.endc} {default_domain}")
print("\n")