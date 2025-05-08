# netfree.py
import requests
import helper
from urllib.parse import urlparse, parse_qs

'''
Supports:
https://netfree.cc/
https://netfree2.cc/
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
base_url = "https://netfree2.cc/mobile/post.php?id=786786&t=1746675074"
hash_cookie = helper.get_cookie();
default_domain = helper.get_main_domain();

# Set-up session for further requests
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://example.com',
})
session.cookies.update({
    't_hash_t': hash_cookie
})

# Fetch response
response = session.get(base_url).json()
title = response.get('title')

# Parse the URL
parsed_url = urlparse(base_url)
query_params = parse_qs(parsed_url.query)

# Get 'id' and 't' parameters
id_param = query_params.get('id', [None])[0]
t_param = query_params.get('t', [None])[0]

# Get Playlists
response = session.get(f'{default_domain}mobile/playlist.php?id={id_param}&t={title}&tm={t_param}').json()
video_sources = response[0].get('sources')

# Get Video URL (Auto Quality)
video_url = None
for item in video_sources:
    if item.get('label') == 'Auto':
        video_url = f'{default_domain}{item.get('file')}'

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)