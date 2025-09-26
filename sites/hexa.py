import re
import random
import requests
from urllib.parse import urlparse

'''
Supports:
https://hexa.watch/
https://flixer.su/
'''

# @Hexa & @Flixer, two birds in one cage :)
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
base_url = "https://flixer.su/watch/tv/110316/1/1"
user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"
decode_api = "https://hexa.yogesh-hacker.deno.net/"
default_domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(base_url))
headers = {
    "Referer": default_domain,
    "Accept": "*/*",
    "User-Agent": user_agent
}

# Get media type and server
media_type = 'movie' if 'movie' in base_url else 'tv'
server = 'hexa' if 'hexa' in base_url else 'flixer'

# Get tmdbId, season and episode
match = re.search(r'/(\d+)(?:/(\d+)/(\d+))?', base_url)
if media_type == "movie":
    media_id = match.group(1)
else:
    media_id = match.group(1)
    season = match.group(2)
    episode = match.group(3)

# Construct URL based on Content Type
if media_type != 'movie':
    decode_url = f'{decode_api}?tmdbId={media_id}&season={season}&episode={episode}&server={server}&mediaType={media_type}'
else:
    decode_url = f'{decode_api}?tmdbId={media_id}&server={server}&mediaType={media_type}'

# Get streaming data
'''
Due to the site's use of WASM, the decryption logic
and WASM implementation are hosted server-side.  
Server-Side Code: https://github.com/yogesh-hacker/yogesh-hacker/tree/main/js/hexa
'''
response = requests.get(decode_url).json()
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