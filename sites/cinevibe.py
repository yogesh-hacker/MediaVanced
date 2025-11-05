import re
import time
import codecs
import base64
import requests
from urllib.parse import urlparse

'''
Supports:
https://cinevibe.asia/
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
base_url = 'https://cinevibe.asia/watch/movie/587412'
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
browser_fingerprint = "eyJzY3JlZW4iOiIzNjB4ODA2eDI0Iiwi"
session_entropy = "pjght152dw2rb.ssst4bzleDI0Iiwibv78"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    'Referer': default_domain,
    'User-Agent': user_agent
}

# Utility Functions
''' A 32-bit FNV-1a Hash Function '''
def fnv1a_32(s):
    t = 2166136261
    for ch in s:
        t ^= ord(ch)
        t = (t + (t << 1) + (t << 4) + (t << 7) + (t << 8) + (t << 24)) & 0xffffffff
    return format(t, "08x")

'''Deterministic string obfuscator using layered reversible encodings'''
def custom_encode(e):
    e = base64.b64encode(e.encode()).decode()
    e = e[::-1]
    e = codecs.encode(e, "rot_13")
    e = base64.b64encode(e.encode()).decode()
    e = e.replace("+", "-").replace("/", "_").replace("=", "")
    return e


# Get media type
media_type = 'movie' if 'movie' in base_url else 'tv'

# Get tmdbId, season and episode
match = re.search(r'/(\d+)(?:/(\d+)/(\d+))?', base_url)
if media_type == "movie":
    media_id = match.group(1)
else:
    media_id = match.group(1)
    season = match.group(2)
    episode = match.group(3)

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

# Construct the token string to be encoded
tmdb_id = data_id
season_id = ""
episode_id = ""
time_based_key = f"{int(time.time() * 1000) // 300000}_{browser_fingerprint}_cinevibe_2025"
token_string = f"{session_entropy}|{tmdb_id}|{re.sub(r'[^a-z0-9]', '', title.lower())}|{release_year}||{fnv1a_32(time_based_key)}|{str(int(time.time() // 600))}|{browser_fingerprint}"

# Generate token and API URL
token = custom_encode(token_string)
api_url = f'{default_domain}api/stream/fetch?server=cinebox-1&type={media_type}&mediaId={tmdb_id}&title={title}&releaseYear={release_year}&_token={token}&_ts={str(int(time.time() * 1000))}'

# Fetch streaming data
get_headers = {
    **headers,
    'X-CV-Fingerprint': browser_fingerprint,
    'X-CV-Session': session_entropy,
    'X-Requested-With': 'XMLHttpRequest'
}
response = requests.get(api_url, headers=get_headers).json()

# Extract video URL
video_url = response.get('sources')[0].get('url')

# Print results
print("\n" + "#" * 25 + "\n" + "#" * 25)
print(f"Captured URL: {Colors.okgreen}{video_url}{Colors.endc}")
print("#" * 25 + "\n" + "#" * 25)
print(f"{Colors.warning}### Use these headers to access the URL")

# Print headers by key: value
for key, value in headers.items():
    print(f"{Colors.okcyan}{key}:{Colors.endc} {value}")
print("\n")